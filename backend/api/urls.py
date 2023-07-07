from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from django.urls import include, path, re_path

from .views import CustomUserViewSet, UserViewSet, UsersView, UserIDView, TagsViewSet, RecipesViewSet, IngridientsViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"recipes", RecipesViewSet, basename="recipes")
router.register(r"ingredients",IngridientsViewSet, basename= "ingredients")


urlpatterns = [
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UserIDView.as_view()),
    path("", include(router.urls)),
]