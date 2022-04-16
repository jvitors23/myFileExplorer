from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from explorer.models import File


@receiver(pre_delete, sender=File)
def create_root_folder(sender, instance, **kwargs):
    # Ensure that file is deleted from S3
    instance.file.delete()


@receiver(pre_save, sender=File)
def delete_old_file(sender, instance, **kwargs):
    # Ensure that old file is deleted from S3
    if instance.id and instance.file:
        instance.size = instance.file.size
        previous_object = File.objects.get(pk=instance.id)
        if previous_object.file and previous_object.file != instance.file:
            previous_object.file.delete()
