from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth.models import AnonymousUser

from .models import Follow, User
from api.models import Recipes


class CustomUserSerializer(UserSerializer):
    password = serializers.CharField(
        min_length=8, max_length=150, write_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        # try:
        user = self.context["request"].user
        if type(user) == AnonymousUser:
            return False
        return user.follower.filter(following=obj).exists()
        # except KeyError:
        #     return False


class RecipesSerializers_2(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "time")


class UserFollowSerializer(serializers.ModelSerializer):
    recipes = RecipesSerializers_2(read_only=True, many=True, source="author")
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
        if type(user) == AnonymousUser:
            return False
        return user.follower.filter(following=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
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
        # following = get_object_or_404(User, id=follow_id)
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
