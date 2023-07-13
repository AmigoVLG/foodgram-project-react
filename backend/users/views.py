from djoser.views import UserViewSet
from rest_framework import generics, viewsets
from users.models import User

from django.shortcuts import get_object_or_404

from .serializers import CustomUserSerializer, FollowSerializer
from api.pagination import CustomPagination


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination


class FollowView(generics.ListCreateAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = user.follower.all()
        return queryset


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        subscribe = self.kwargs.get("id")
        queryset = user.follower.filter(following=subscribe)
        return queryset

    def perform_create(self, serializer):
        subscribe = self.kwargs.get("id")
        following = get_object_or_404(User, id=subscribe)
        serializer.save(user=self.request.user, following=following)
