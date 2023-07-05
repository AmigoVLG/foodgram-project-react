from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import mixins, status, viewsets

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics

from .models import User


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

