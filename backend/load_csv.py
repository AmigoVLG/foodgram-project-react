from csv import DictReader

from django.core.management import BaseCommand

from .models import Ingredient


class Command(BaseCommand):
    """
    Перед запуском удалите файл db.sqlite3 в корневой директории
    Запустите команду python manage.py migrate --run-syncdb
    Запустите импорт команду python manage.py load_csv
    """

    help = "Импорт .csv в Django Database"

    def handle(self, *args, **kwargs):
        for row in DictReader(open("data/ingredients.csv", encoding="utf-8")):
            ingredient = Ingredient(
                name=row["name"],
                measurement_unit=row["measurement_unit"]

            )
            ingredient.save()