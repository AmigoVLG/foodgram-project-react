from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CustomUserViewSet, FollowView, SubscribeViewSet

router = DefaultRouter()
router.register("", CustomUserViewSet)
router.register(
    r"(?P<id>[0-9]+)/subscribe", SubscribeViewSet, basename="Subscribers"
)


urlpatterns = [
    path("subscriptions/", FollowView.as_view()),
    path("", include(router.urls)),
]
