from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "count_favorites")
    search_fields = ("name", "author")
    list_filter = (
        "name",
        "author",
        "tags",
    )
    inlines = [RecipeTagsInLine, RecipeIngredientsInLine]

    def get_queryset(self, request):
        queryset = (
            Recipe.objects.all()
            .select_related("author")
            .prefetch_related("tags", "ingredients")
        )
        return queryset

    def count_favorites(self, request):
        count = request.favorites
        return count.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_editable = ("name", "unit")
    list_display = ("id", "name", "unit")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_editable = ("name", "color", "slug")
    list_display = ("id", "name", "color", "slug")
