from django.db.models.signals import pre_delete
from django.dispatch import receiver
from explorer.models import File


@receiver(pre_delete, sender=File)
def delete_s3_file(sender, instance, **kwargs):
    # Ensure that file is deleted from S3
    instance.file.delete()
