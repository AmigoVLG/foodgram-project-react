from rest_framework import serializers

from django.shortcuts import get_object_or_404

from djoser.serializers import UserSerializer

from rest_framework.validators import UniqueTogetherValidator

from .models import User, Ingredient, Tag, Recipes, TagRecipes, IngredientRecipes, Follow

import base64

from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CustomUserSerializer(UserSerializer):
    password = serializers.CharField(min_length=8, max_length=150, write_only=True)
    is_subscribed = serializers.SerializerMethodField()
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name','is_subscribed','password')
        required_fields = ['email']
    
    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return user.follower.filter(following=obj).exists()

class IngredientRecipesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='ingredient')
    id = serializers.SerializerMethodField(source='kora')
    
    class Meta:
        model = IngredientRecipes
        fields = ('id','name', 'amount','unit')

    def get_id(self,obj):
        return obj.ingredient.id
        

class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(source='unit')
    class Meta:
        model = Ingredient
        fields = ('id','name', 'measurement_unit')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name', 'color','slug')

class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipesSerializer(many=True,read_only=True, source='products')
    image = Base64ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Recipes
        fields = ('id','author', 'name', 'image','text','tags','time','pub_date', 'ingredients')
    
    def create(self, validated_data):
        tags = self.initial_data['tags']
        ingridients = self.initial_data['products']
        recipes = Recipes.objects.create(**validated_data)
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag)
            TagRecipes.objects.create(
                tag=current_tag, name=recipes
            )
        for ingridient in ingridients:
            current_ingredient = get_object_or_404(Ingredient, id=ingridient['id'])
            IngredientRecipes.objects.create(
                ingredient=current_ingredient,
                name=recipes,
                amount=ingridient['amount'],
                unit=current_ingredient.unit
            )
        return recipes
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.time = validated_data.get(
            'time', instance.time
        )
        instance.image = validated_data.get('image', instance.image)
        tags_data = self.initial_data['tags']
        ingridients_data = self.initial_data['products']
        lst = []
        for tag in tags_data:
            current_tag = get_object_or_404(Tag, id=tag)
            lst.append(current_tag)
        instance.tags.set(lst)
        lst_2 = []
        for ingridient in ingridients_data:
            current_ingredient = get_object_or_404(Ingredient, id=ingridient['id'])
            lst_2.append(current_ingredient)
        instance.ingredients.set(lst_2)
        instance.save()
        return instance


class RecipesSerializers_2(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id','name', 'image','time')

class UserFollowSerializer(serializers.ModelSerializer):
    recipes = RecipesSerializers_2(read_only=True, many=True, source='author')
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name','is_subscribed', 'recipes', 'recipes_count')
    def get_recipes_count(self,obj):
        return obj.author.count()
        
    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return user.follower.filter(following=obj).exists()

class FollowSerializer(serializers.ModelSerializer):
    following = UserFollowSerializer(default=None)
    user = serializers.CharField(write_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Follow
        fields = ["following",'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]
    def validate(self, data):
        request = self.context.get("request")
        follow_id = self.context.get("view").kwargs.get("id")
        following = get_object_or_404(User, id=follow_id)
        if (
            request.method == "POST"
            and Follow.objects.filter(
                user=request.user.id, following=int(follow_id)
            ).exists()
        ):
            raise serializers.ValidationError(
                "уже подписан"
            )
        if (request.method == "POST"
            and request.user == following):
            raise serializers.ValidationError("нельзя подписаться на самого себя")
        return data
