from django.contrib import admin

from .models import Follow, User


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following")

    def get_queryset(self, request):
        queryset = Follow.objects.select_related("user", "following")
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
