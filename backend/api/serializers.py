import base64

from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from recipes.models import (
    FavoritRecipe,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    """ " Сериализатор пользователя."""

    password = serializers.CharField(
        min_length=8, max_length=150, write_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "password",
        )
        required_fields = ["email"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.follower.filter(following=obj).exists()
        return False


class Base64ImageField(serializers.ImageField):
    """Сериализатор изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class IngredientRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для связи ингридиентов, рецептов и количества."""

    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.StringRelatedField(read_only=True, source="ingredient")
    measurement_unit = serializers.CharField(source="unit")

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "amount", "measurement_unit")


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингридиентов."""

    measurement_unit = serializers.CharField(source="unit")

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class RecipesSerializer(serializers.ModelSerializer):
    """Главный сериализатор рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipesSerializer(
        many=True, read_only=True, source="products"
    )
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(source="time")

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "name",
            "image",
            "text",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
            "cooking_time",
            "ingredients",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.shopping.filter(user=user).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False

    def validate(self, data):
        """Проверка наличия тегов, ингредиентов и времени приготовления."""
        if self.initial_data["tags"] == []:
            raise serializers.ValidationError("минимум один тег обязателен")
        if data.get("time") <= 0:
            raise serializers.ValidationError(
                "время приготовления не может быть нулевым и отрицательным"
            )
        if self.initial_data["ingredients"] == []:
            raise serializers.ValidationError("ингредиенты обязательны")
        return data

    def add_tag_ingredient(
        self, ingredients: list, instance: Recipe, tags: list
    ) -> None:
        """Функция добавления ингридиентов и тегов в рецепт."""
        tag_update_list = []
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag)
            tag_update_list.append(current_tag)
        instance.tags.set(tag_update_list)
        instance.save()
        IngredientRecipe.objects.filter(name=instance).delete()
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient["id"]
            )
            IngredientRecipe.objects.update_or_create(
                name_id=instance.id,
                ingredient_id=current_ingredient.id,
                amount=ingredient["amount"],
                unit=current_ingredient.unit,
            )

    def create(self, validated_data):
        """создание рецепта."""
        tags = self.initial_data["tags"]
        ingredients = self.initial_data["ingredients"]
        recipes = Recipe.objects.create(**validated_data)
        self.add_tag_ingredient(ingredients, recipes, tags)
        return recipes

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        tags_data = self.initial_data["tags"]
        ingredients_data = self.initial_data["ingredients"]
        self.add_tag_ingredient(ingredients_data, instance, tags_data)
        return super().update(instance, validated_data)


class MiniRecipesSerializers(serializers.ModelSerializer):
    """Сериализатор рецептов для предпросмотра."""

    cooking_time = serializers.IntegerField(source="time")

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избраного."""

    user = serializers.CharField(write_only=True, default=None)
    recipes = MiniRecipesSerializers(default=None)

    class Meta:
        model = FavoritRecipe
        fields = ("user", "recipes")
        validators = [
            UniqueTogetherValidator(
                queryset=FavoritRecipe.objects.all(),
                fields=("user", "recipes"),
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        recipes_id = self.context.get("view").kwargs.get("id")
        if (
            request.method == "POST"
            and FavoritRecipe.objects.filter(
                user=request.user.id, recipes=int(recipes_id)
            ).exists()
        ):
            raise serializers.ValidationError("уже добавлен")
	return data


class ShoppingSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    user = serializers.CharField(write_only=True, default=None)
    recipes = MiniRecipesSerializers(default=None)

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipes")
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(), fields=("user", "recipes")
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        recipes_id = self.context.get("view").kwargs.get("id")
        if (
            request.method == "POST"
            and ShoppingCart.objects.filter(
                user=request.user.id, recipes=int(recipes_id)
            ).exists()
        ):
            raise serializers.ValidationError("уже добавлен")
        return data


class UserFollowSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра подписок."""

    recipes = MiniRecipesSerializers(
        read_only=True, many=True, source="author"
    )
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return obj.author.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.follower.filter(following=obj).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор добавления и удаления подписок."""

    following = UserFollowSerializer(default=None)
    user = serializers.CharField(write_only=True, default=None)

    class Meta:
        model = Follow
        fields = ["following", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        follow_id = self.context.get("view").kwargs.get("id")
        if (
            request.method == "POST"
            and Follow.objects.filter(
                user=request.user.id, following=int(follow_id)
            ).exists()
        ):
            raise serializers.ValidationError("уже подписан")
        if request.method == "POST" and request.user.id == int(follow_id):
            raise serializers.ValidationError(
                "нельзя подписаться на самого себя"
            )
        return data
