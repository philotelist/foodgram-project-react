from django.db.models import Sum

# from api.models import IngredientQuantity


def get_cart(ingredients):
    return ('\n'.join([
        f'{ingredient["ingredients__name"]} - {ingredient["total"]} '
        f'{ingredient["ingredients__measurement_unit"]}'
        for ingredient in ingredients])
    )