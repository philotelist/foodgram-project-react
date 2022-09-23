from api.models import IngredientQuantity


def ingredients_list(self, request):
    ingredients = IngredientQuantity.objects.filter(
        recipe__shopping_carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit', 'amount')
    return ('\n'.join([
                f'{ingredient["ingredient__name"]} - {ingredient["amount"]}'
                f'{ingredient["ingredient__measurement_unit"]}'
                for ingredient in ingredients])
    )
