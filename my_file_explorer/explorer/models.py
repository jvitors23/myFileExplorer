import os
import uuid

from django.conf import settings
from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Folder(BaseModel):

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', null=True,
                                      on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'parent_folder', 'owner')

    def get_children_folders(self):
        return Folder.objects.filter(parent_folder=self)

    def get_children_files(self):
        return File.objects.filter(parent_folder=self)

    @staticmethod
    def can_place_in_folder(parent_folder, name, instance=None) -> bool:
        folders_same_folder = Folder.objects.filter(
            parent_folder=parent_folder
        )
        if instance:
            folders_same_folder = folders_same_folder.exclude(
                pk=instance.id
            )
        return not folders_same_folder.filter(name=name).exists()


def get_s3_file_path(instance, filename):
    user = instance.owner.username
    parent_folder = instance.parent_folder.name
    name, extension = os.path.splitext(filename)
    return f'{user}/{parent_folder}/{uuid.uuid4()}{extension}'


class File(BaseModel):

    name = models.CharField(max_length=30)
    parent_folder = models.ForeignKey('explorer.Folder', null=False,
                                      on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_s3_file_path)
    size = models.PositiveIntegerField()

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'parent_folder', 'owner')

    @staticmethod
    def can_place_in_folder(parent_folder, name, instance=None) -> bool:
        files_same_folder = File.objects.filter(parent_folder=parent_folder)
        if instance:
            files_same_folder = files_same_folder.exclude(pk=instance.id)
        return not files_same_folder.filter(name=name).exists()
