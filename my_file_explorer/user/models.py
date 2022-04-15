from django.db import models

from django.contrib.auth.models import PermissionsMixin, AbstractUser


from explorer.models import Folder


class User(AbstractUser):
    """Custom user model"""
    root_folder = models.ForeignKey('explorer.Folder', on_delete=models.CASCADE, null=True)

    def create_root_folder(self):
        root_folder = Folder(name=f'root_folder_user_{self.id}', owner=self)
        root_folder.save()
        self.root_folder = root_folder
        self.save()
