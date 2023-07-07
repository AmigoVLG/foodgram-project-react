from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, UserSerializer, RecipesSerializer, TagSerializer, IngredientSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import mixins, status, viewsets
from .permissions import PermissionDenied
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import User, Tag, Recipes, Ingredient


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
