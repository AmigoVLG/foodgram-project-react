# Generated by Django 3.2.3 on 2023-07-06 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20230706_1230'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingridient',
            new_name='Ingredient',
        ),
        migrations.RenameModel(
            old_name='IngridientRecipes',
            new_name='IngredientRecipes',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='ingridients',
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(through='api.IngredientRecipes', to='api.Ingredient'),
        ),
    ]
