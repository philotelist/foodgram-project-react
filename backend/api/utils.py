from django.db.models import Sum

from api.models import IngredientQuantity


def ingredients_list(request):
    ingredients = IngredientQuantity.objects.filter(
        recipe__shopping_cart__user=request.user).values(
            'ingredients__name',
            'ingredients__measurement_unit').annotate(total=Sum('amount')
    )
    cart = '\n'.join([
        f'{ingredient["ingredients__name"]} - {ingredient["total"]} '
        f'{ingredient["ingredients__measurement_unit"]}'
        for ingredient in ingredients
    ])
    return cart
