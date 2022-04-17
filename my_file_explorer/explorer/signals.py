from django.db.models.signals import pre_delete
from django.dispatch import receiver
from explorer.models import File


@receiver(pre_delete, sender=File)
def create_root_folder(sender, instance, **kwargs):
    # Ensure that file is deleted from S3
    instance.file.delete()
