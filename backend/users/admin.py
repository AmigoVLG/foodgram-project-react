from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag
from users.models import Follow, User


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following")

    def get_queryset(self, request):
        queryset = Follow.objects.all().select_related("user", "following")
        return queryset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_editable = ("username",)
    search_fields = ("username", "email")
    list_filter = (
        "username",
        "email",
    )


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
