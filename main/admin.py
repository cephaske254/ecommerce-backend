from django.contrib import admin
from .models import accounts
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
class UserAdmin(DefaultUserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "email_verified",
        "is_active",
        "is_superuser",
        "last_login",
    ]
    ordering = ["full_name", "email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("date_joined", "email_verified")
    list_filter = ("email_verified", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("full_name", "email")


admin.site.register(accounts.User, UserAdmin)
