import base64

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CustomUserSerializer

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from .models import (
    Favorit,
    Ingredient,
    IngredientRecipes,
    Recipes,
    Shopping,
    Tag,
    TagRecipes,
    User,
)


class Base64ImageField(serializers.ImageField):
    """Сериализатор изображений"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class IngredientRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для связи ингридиентов рецептов и количества"""

    name = serializers.SlugRelatedField(read_only=True, slug_field="name")
    id = serializers.SerializerMethodField(source="kora")

    class Meta:
        model = IngredientRecipes
        fields = ("id", "name", "amount", "unit")

    def get_id(self, obj):
        return obj.ingredient.id


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингридиентов"""

    measurement_unit = serializers.CharField(source="unit")

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тегов"""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class RecipesSerializer(serializers.ModelSerializer):
    """Главный сериализатор рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipesSerializer(
        many=True, read_only=True, source="products"
    )
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            "id",
            "author",
            "name",
            "image",
            "text",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
            "time",
            "ingredients",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if type(user) == AnonymousUser:
            return False
        return obj.shopping.filter(user=user).exists()

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if type(user) == AnonymousUser:
            return False
        return obj.favorites.filter(user=user).exists()

    def create(self, validated_data):
        tags = self.initial_data["tags"]
        ingridients = self.initial_data["ingredients"]
        recipes = Recipes.objects.create(**validated_data)
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag)
            TagRecipes.objects.create(tag=current_tag, name=recipes)
        for ingridient in ingridients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingridient["id"]
            )
            IngredientRecipes.objects.create(
                ingredient=current_ingredient,
                name=recipes,
                amount=ingridient["amount"],
                unit=current_ingredient.unit,
            )
        return recipes

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.time = validated_data.get("time", instance.time)
        instance.image = validated_data.get("image", instance.image)
        tags_data = self.initial_data["tags"]
        ingridients_data = self.initial_data["ingredients"]
        lst = []
        for tag in tags_data:
            current_tag = get_object_or_404(Tag, id=tag)
            lst.append(current_tag)
        instance.tags.set(lst)
        lst_2 = []
        for ingridient in ingridients_data:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingridient["id"]
            )
            lst_2.append(current_ingredient)
        instance.ingredients.set(lst_2)
        instance.save()
        return instance


class MiniRecipesSerializers(serializers.ModelSerializer):
    """Сериализатор рецептов для предпросмотра"""

    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "time")


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""

    user = serializers.CharField(write_only=True, default=None)
    recipes = MiniRecipesSerializers(default=None)

    class Meta:
        model = Favorit
        fields = ("user", "recipes")
        validators = [
            UniqueTogetherValidator(
                queryset=Favorit.objects.all(), fields=("user", "recipes")
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        recipes_id = self.context.get("view").kwargs.get("id")
        user_recipes = get_object_or_404(User, author=recipes_id)
        if (
            request.method == "POST"
            and Favorit.objects.filter(
                user=request.user.id, recipes=int(recipes_id)
            ).exists()
        ):
            raise serializers.ValidationError("уже добавлен")
        if request.method == "POST" and request.user == user_recipes:
            raise serializers.ValidationError("зачем добавлять свой рецепт?")
        return data


class ShoppingSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок"""

    user = serializers.CharField(write_only=True, default=None)
    recipes = MiniRecipesSerializers(default=None)

    class Meta:
        model = Shopping
        fields = ("user", "recipes")
        validators = [
            UniqueTogetherValidator(
                queryset=Shopping.objects.all(), fields=("user", "recipes")
            )
        ]

    def validate(self, data):
        request = self.context.get("request")
        recipes_id = self.context.get("view").kwargs.get("id")
        if (
            request.method == "POST"
            and Shopping.objects.filter(
                user=request.user.id, recipes=int(recipes_id)
            ).exists()
        ):
            raise serializers.ValidationError("уже добавлен")
        return data
