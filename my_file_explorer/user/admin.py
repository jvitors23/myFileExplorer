from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'first_name', 'is_superuser', 'is_active']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('root_folder',)}),
    )


admin.site.register(models.User, UserAdmin)
