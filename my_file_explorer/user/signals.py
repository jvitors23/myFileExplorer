from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=User)
def create_root_folder(sender, instance, **kwargs):
    if not instance.root_folder:
        instance.create_root_folder()
