from django.contrib import admin

from explorer import models


class FolderAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'parent_folder', 'owner']


class FileAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'parent_folder', 'owner']


admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.File, FileAdmin)

