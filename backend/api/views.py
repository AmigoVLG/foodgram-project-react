from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipesFilter
from .models import (
    Favorit,
    Ingredient,
    IngredientRecipes,
    Recipes,
    Shopping,
    Tag,
)
from .permissions import PermissionDenied
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipesSerializer,
    ShoppingSerializer,
    TagSerializer,
)


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class RecipesViewSet(viewsets.ModelViewSet):
    """CRUD рецептов и выгрузка списка покупок"""

    queryset = Recipes.objects.all()
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
        print("perform_create")
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
        shopping_cart = Shopping.objects.filter(user=user)
        cart = {}
        for goods in shopping_cart:
            x = goods.recipes.id
            recipes = IngredientRecipes.objects.filter(name_id=x)
            for recipe in recipes:
                if recipe.ingredient.name in cart:
                    cart[recipe.ingredient.name][0] += recipe.amount
                else:
                    cart[recipe.ingredient.name] = [recipe.amount, recipe.unit]

        response = HttpResponse(
            cart.items(),
            {
                "Content-Type": "text/plain",
                "Content-Disposition": 'attachment; filename="out_list.txt"',
            },
        )
        return response


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
        favorit = get_object_or_404(Recipes, id=recipes)
        serializer.save(user=self.request.user, recipes=favorit)

    def delete(self, request, id=None):
        favorit = get_object_or_404(Recipes, id=id)
        instance = get_object_or_404(Favorit, recipes=favorit)
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
        shopping = get_object_or_404(Recipes, id=recipes)
        serializer.save(user=self.request.user, recipes=shopping)

    def delete(self, request, id=None):
        shopping = get_object_or_404(Recipes, id=id)
        instance = get_object_or_404(Shopping, recipes=shopping)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
