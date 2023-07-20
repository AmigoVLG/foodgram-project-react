from django.db.models.query import QuerySet
from django.http import HttpResponse

from recipes.models import ShoppingCart


def create_shopping_cart(
    ingredients_cart: QuerySet[ShoppingCart],
) -> HttpResponse:
    """Формируем список покупок из запроса в файл."""

    shopping_cart = "\n".join(
        [
            f'{i["ingredient__name"]} ' f'({i["unit"]}) – ' f'{i["amount"]}'
            for i in ingredients_cart
        ]
    )
    response = HttpResponse(
        shopping_cart,
        {
            "Content-Type": "text/plain",
            "Content-Disposition": 'attachment; filename="out_list.txt"',
        },
    )
    return response
