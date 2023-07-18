from django.http import HttpResponse


def create_shopping_cart(ingredients_cart):
    """Формируем список покупок из запроса в файл"""
    print(ingredients_cart.values_list)

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
