from users.models import User

from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=16)


class Tag(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=16)
    slug = models.CharField(max_length=16)


class Recipes(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    name = models.CharField(max_length=120)
    image = models.ImageField(
        upload_to="foods/images/", null=True, default=None
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientRecipes"
    )
    tags = models.ManyToManyField(Tag, through="TagRecipes")
    time = models.CharField(max_length=12)
    pub_date = models.DateTimeField(auto_now_add=True)


class IngredientRecipes(models.Model):
    name = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="products"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.CharField(max_length=36)

    def __str__(self):
        return self.name, self.ingredient, self.unit


class TagRecipes(models.Model):
    name = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="favorites"
    )


class Shopping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="shopping"
    )
