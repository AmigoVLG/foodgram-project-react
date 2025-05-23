from csv import reader

from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    """
    Перед запуском удалите файл db.sqlite3 в корневой директории
    Запустите команду python manage.py migrate --run-syncdb
    Запустите импорт команду python manage.py load_csv
    """

    help = "Импорт .csv в Django Database"

    def handle(self, *args, **kwargs):
        for row in reader(open("data/ingredients.csv", encoding="utf-8")):
            ingredient = Ingredient(name=row[0], unit=row[1])
            ingredient.save()

        for line in reader(open("data/tags.csv", encoding="utf-8")):
            tag = Tag(name=line[0], color=line[1], slug=line[2])
            tag.save()
