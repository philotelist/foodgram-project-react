from django.db.models import Sum

from .models import IngredientQuantity


def get_cart(request):
    ingredients = IngredientQuantity.objects.filter(
            recipe__shopping_carts__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit',).annotate(
            amount=Sum('amount')).order_by()
    return (
        '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
    )
