from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from django.urls import include, path, re_path

from .views import CustomUserViewSet, UserViewSet, UsersView, UserIDView

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UserIDView.as_view()),
    path("", include(router.urls)),
]