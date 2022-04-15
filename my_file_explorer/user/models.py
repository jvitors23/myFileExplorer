from django.db import models

from django.contrib.auth.models import PermissionsMixin, AbstractUser


class User(AbstractUser):
    """Custom user model"""
    root_folder = models.ForeignKey('explorer.Folder', on_delete=models.CASCADE, null=True)
