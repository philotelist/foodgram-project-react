def get_cart(ingredients):
    return ('\n'.join([
        f'{ingredient["ingredient__name"]} - {ingredient["total"]} '
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients])
    )
