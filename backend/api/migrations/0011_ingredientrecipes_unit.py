# Generated by Django 3.2.3 on 2023-07-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_ingredientrecipes_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientrecipes',
            name='unit',
            field=models.CharField(default=1, max_length=36),
            preserve_default=False,
        ),
    ]
