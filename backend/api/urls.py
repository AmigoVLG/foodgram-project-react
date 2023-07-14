from rest_framework.routers import DefaultRouter

from django.urls import include, path, re_path

from .views import (
    FavoriteViewSet, IngridientsViewSet, RecipesViewSet, ShoppingViewSet,
    TagsViewSet,
)

router = DefaultRouter()
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"recipes", RecipesViewSet, basename="recipes")
router.register(r"ingredients", IngridientsViewSet, basename="ingredients")
router.register(
    r"recipes/(?P<id>[0-9]+)/favorite", FavoriteViewSet, basename="favorite"
)
router.register(
    r"recipes/(?P<id>[0-9]+)/shopping_cart",
    ShoppingViewSet,
    basename="shopping",
)


urlpatterns = [
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
