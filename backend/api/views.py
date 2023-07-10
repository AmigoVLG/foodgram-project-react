from djoser.views import UserViewSet
from .serializers import (
    CustomUserSerializer, UserSerializer, RecipesSerializer,
    TagSerializer, IngredientSerializer, FollowSerializer,
    FavoriteSerializer, ShoppingSerializer
    )
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import mixins, status, viewsets
from .permissions import PermissionDenied
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import action

from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import User, Tag, Recipes, Ingredient, Follow, Favorit, Shopping


from rest_framework import mixins


class ListRetrieveViewSet(
        mixins.ListModelMixin, 
        mixins.RetrieveModelMixin, 
        viewsets.GenericViewSet):
    pass

class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
class UserIDView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class FollowView(generics.ListCreateAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = user.follower.all()
        return queryset

class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = User.objects.all()
    # def get_queryset(self):
    #     user = get_object_or_404(User, id=self.request.user.id)
    #     subscribe = self.kwargs.get('id')
    #     queryset = user.follower.filter(following=subscribe)
    #     return queryset

    def perform_create(self, serializer):
        subscribe = self.kwargs.get('id')
        following = get_object_or_404(User, id=subscribe)
        serializer.save(user=self.request.user, following=following)



class TagsViewSet(ListRetrieveViewSet):
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (
        PermissionDenied,
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngridientsViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    def perform_create(self, serializer):
        recipes = self.kwargs.get('id')
        favorit = get_object_or_404(Recipes, id=recipes)
        serializer.save(user=self.request.user, recipes=favorit)


    def delete(self, request, id=None):

        favorit = get_object_or_404(Recipes, id=id)
        instance = get_object_or_404(Favorit, recipes=favorit)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingSerializer
    def perform_create(self, serializer):
        recipes = self.kwargs.get('id')
        shopping = get_object_or_404(Recipes, id=recipes)
        serializer.save(user=self.request.user, recipes=shopping)


    def delete(self, request, id=None):

        shopping = get_object_or_404(Recipes, id=id)
        instance = get_object_or_404(Shopping, recipes=shopping)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
