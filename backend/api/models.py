from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='Название тега'
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код', unique=True, max_length=7,
        validators=[
            RegexValidator(
                r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Неправильный формат!'
            )
        ]
    )
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=100, verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта'
    )
    name = models.CharField(max_length=100, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/', verbose_name='Картинка рецепта'
    )
    text = models.TextField(max_length=200, verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientQuantity', verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1, message='Время приготовления должно быть больше 0!'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(
            1, 'Минимальное количество ингридиентов 1'),
        ],
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_ingredients_ in_recipe')
        ]

    def str(self):
        return f'{self.ingredient.name} - {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_carts', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_carts', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_cart'
            )
        ]
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
