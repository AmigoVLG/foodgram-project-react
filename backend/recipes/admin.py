from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import admin

from .models import Ingredient, Recipe, Tag, ShoppingCart


class AuthorFilter(AutocompleteFilter):
    title = "Author"
    field_name = "author"


class ShoppingCartFilter(AutocompleteFilter):
    title = "Recipes"
    field_name = "recipes"


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "count_favorites")
    search_fields = ("name",)
    list_filter = ("tags", AuthorFilter,)
    inlines = [RecipeTagsInLine, RecipeIngredientsInLine]

    def get_queryset(self, request):
        queryset = Recipe.objects.select_related("author").prefetch_related(
            "tags", "ingredients"
        )
        return queryset

    def count_favorites(self, request):
        count = request.favorites
        return count.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color", "slug")
    search_fields = ("name",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipes")
    search_fields = ("user",)
    list_filter = [ShoppingCartFilter]
