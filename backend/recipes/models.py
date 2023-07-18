from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField("ингредиент", max_length=150)
    unit = models.CharField("единица измерения", max_length=150)

    class Meta:
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("тег", max_length=150)
    color = models.CharField("цвет", max_length=16)
    slug = models.CharField("tag_slug", max_length=64)

    class Meta:
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    name = models.CharField("навазение рецепта", max_length=150)
    image = models.ImageField(
        "изображение", upload_to="foods/images/", null=True, default=None
    )
    text = models.TextField("описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        related_name="recipes",
        verbose_name="ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag, through="TagRecipe", related_name="recipes", verbose_name="теги"
    )
    time = models.IntegerField("время приготовления")
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания"
    )

    class Meta:
        verbose_name_plural = "Рецепты"


class IngredientRecipe(models.Model):
    name = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="products"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="components"
    )
    amount = models.IntegerField()
    unit = models.CharField(max_length=150)

    def __str__(self):
        return self.ingredient


class TagRecipe(models.Model):
    name = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="tagrecipe"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tagrecipe"
    )


class FavoritRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite"
    )
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping"
    )
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shopping"
    )
