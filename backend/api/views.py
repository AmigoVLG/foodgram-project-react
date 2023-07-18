from djoser.views import UserViewSet
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from recipes.models import (
    FavoritRecipe,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Follow, User
from .utils import create_shopping_cart
from .filters import RecipesFilter
from .pagination import CustomPagination
from .permissions import PermissionDenied
from .serializers import (
    CustomUserSerializer,
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipesSerializer,
    ShoppingSerializer,
    TagSerializer,
    UserFollowSerializer,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination


class FollowView(generics.ListAPIView):
    """Просмотр подписок"""

    serializer_class = UserFollowSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(following__user=user).annotate(
            recipes_count=Count("author")
        )
        return queryset


class SubscribeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Добавление и удаление подписок"""

    serializer_class = FollowSerializer
    queryset = User.objects.all().annotate(recipes_count=Count("author"))

    def perform_create(self, serializer, id=None):
        subscribe = self.kwargs.get("id")
        following = get_object_or_404(User, id=subscribe)
        serializer.save(user=self.request.user, following=following)

    def delete(self, request, id=None):
        follower = get_object_or_404(User, id=id)
        instance = get_object_or_404(
            Follow, user=self.request.user, following=follower
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class RecipesViewSet(viewsets.ModelViewSet):
    """CRUD рецептов и выгрузка списка покупок"""

    queryset = (
        Recipe.objects.all()
        .select_related("author")
        .prefetch_related("tags", "ingredients")
    )
    serializer_class = RecipesSerializer
    permission_classes = (
        PermissionDenied,
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        "name",
        "tags",
        "id",
    )

    ordering = ("-pub_date",)
    ordering_fields = ("pub_date",)
    search_fields = ("name",)
    filterset_class = RecipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(IsAuthenticated,),
        serializer_class=RecipesSerializer,
        url_path="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_query = IngredientRecipe.objects.filter(
            name__shopping__user=user
        )
        shopping_cart = (
            shopping_query.values_list()
            .values("ingredient__name", "unit")
            .annotate(amount=Sum("amount"))
        )

        # cart = {}
        # for goods in shopping_cart:
        #     x = goods.recipes.id
        #     recipes = IngredientRecipe.objects.filter(name_id=x)
        #     for recipe in recipes:
        #         if recipe.ingredient.name in cart:
        #             cart[recipe.ingredient.name][0] += recipe.amount
        #         else:
        #             cart[recipe.ingredient.name] = [recipe.amount, recipe.unit]

        # response = HttpResponse(
        #     shopping_cart,
        #     {
        #         "Content-Type": "text/plain",
        #         "Content-Disposition": 'attachment; filename="out_list.txt"',
        #     },
        # )
        return create_shopping_cart(shopping_cart)


class TagsViewSet(ListRetrieveViewSet):
    """Получение одного или списка тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientsViewSet(ListRetrieveViewSet):
    """Получение одного или списка ингридиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Добавление и удаление избранных рецептов"""

    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipes = self.kwargs.get("id")
        favorit = get_object_or_404(Recipe, id=recipes)
        serializer.save(user=self.request.user, recipes=favorit)

    def delete(self, request, id=None):
        favorit = get_object_or_404(Recipe, id=id)
        instance = get_object_or_404(FavoritRecipe, recipes=favorit)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Добавление и удаление в списке покупок"""

    serializer_class = ShoppingSerializer

    def perform_create(self, serializer, pk=None):
        recipes = self.kwargs.get("id")
        shopping = get_object_or_404(Recipe, id=recipes)
        serializer.save(user=self.request.user, recipes=shopping)

    def delete(self, request, id=None):
        shopping = get_object_or_404(Recipe, id=id)
        instance = get_object_or_404(ShoppingCart, recipes=shopping)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
