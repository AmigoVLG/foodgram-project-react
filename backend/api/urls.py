from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from django.urls import include, path, re_path

from .views import( CustomUserViewSet, UserViewSet,
                    UsersView, UserIDView, TagsViewSet, RecipesViewSet, 
                    IngridientsViewSet, FollowView, 
                    SubscribeViewSet, FavoriteViewSet, ShoppingViewSet
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")
router.register(
    r"users/(?P<id>[0-9]+)/subscribe", SubscribeViewSet, basename="Subscribers")
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"recipes", RecipesViewSet, basename="recipes")
router.register(r"ingredients",IngridientsViewSet, basename= "ingredients")
router.register(
    r"recipes/(?P<id>[0-9]+)/favorite", FavoriteViewSet, basename="favorite")
router.register(
    r"recipes/(?P<id>[0-9]+)/shopping_cart", ShoppingViewSet, basename="shopping")


urlpatterns = [
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UserIDView.as_view()),
    path ('subscriptions/', FollowView.as_view()),
    # path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path("", include(router.urls)),
]
