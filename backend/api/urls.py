from rest_framework.routers import DefaultRouter

from django.urls import include, path, re_path

from .views import (
    CustomUserViewSet,
    FavoriteViewSet,
    FollowView,
    IngridientsViewSet,
    RecipesViewSet,
    ShoppingViewSet,
    SubscribeViewSet,
    TagsViewSet,
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")
router.register(
    r"users/(?P<id>[0-9]+)/subscribe", SubscribeViewSet, basename="subscribers"
)
router.register(r"recipes", RecipesViewSet, basename="recipes")
router.register(
    r"recipes/(?P<id>[0-9]+)/favorite", FavoriteViewSet, basename="favorite"
)
router.register(
    r"recipes/(?P<id>[0-9]+)/shopping_cart",
    ShoppingViewSet,
    basename="shopping",
)
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"ingredients", IngridientsViewSet, basename="ingredients")


urlpatterns = [
    path("users/subscriptions/", FollowView.as_view()),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
