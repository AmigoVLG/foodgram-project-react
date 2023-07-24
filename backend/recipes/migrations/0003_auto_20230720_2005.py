# Generated by Django 3.2.3 on 2023-07-20 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={"verbose_name_plural": "Ингредиенты"},
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={"verbose_name_plural": "Рецепты"},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name_plural": "Теги"},
        ),
        migrations.RemoveField(
            model_name="ingredientrecipe",
            name="unit",
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=150, verbose_name="ингредиент"),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="unit",
            field=models.CharField(
                max_length=150, verbose_name="единица измерения"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                default=None,
                null=True,
                upload_to="foods/images/",
                verbose_name="изображение",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="recipes",
                through="recipes.IngredientRecipe",
                to="recipes.Ingredient",
                verbose_name="ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(
                max_length=150, verbose_name="навазение рецепта"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="дата создания"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipes",
                through="recipes.TagRecipe",
                to="recipes.Tag",
                verbose_name="теги",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="text",
            field=models.TextField(verbose_name="описание рецепта"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="time",
            field=models.IntegerField(verbose_name="время приготовления"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(max_length=16, verbose_name="цвет"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=150, verbose_name="тег"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.CharField(max_length=64, verbose_name="tag_slug"),
        ),
    ]
