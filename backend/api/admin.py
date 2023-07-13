from users.models import User

from django.contrib import admin

from .models import Ingredient, Recipes, Tag


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


class RecipesAdmin(admin.ModelAdmin):
    def count_favorites(self, request):
        count = request.favorites
        return count.count()

    list_display = ("id", "name", "author", "count_favorites")
    list_filter = (
        "name",
        "author",
        "tags",
    )


class IngredientAdmin(admin.ModelAdmin):
    list_editable = ("name", "unit")
    list_display = ("id", "name", "unit")
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_editable = ("name", "color", "slug")
    list_display = ("id", "name", "color", "slug")


admin.site.register(User, UserAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
