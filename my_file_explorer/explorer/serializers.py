from rest_framework import serializers

from explorer.models import Folder
from rest_framework.exceptions import PermissionDenied, ValidationError


class FolderBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def validate_name(self, name):
        invalid_character = {c for c in name if not c.isalnum()}
        if invalid_character:
            raise serializers.ValidationError(
                f'Name can\'t have {invalid_character}'
            )
        return name

    def validate_parent_folder(self, parent_folder):
        if parent_folder.owner != self.instance.owner:
            raise PermissionDenied()
        return parent_folder

    def validate(self, attrs):
        if self.instance.parent_folder is None:
            # User can't edit the root folder
            raise PermissionDenied()

        new_name = attrs.get('name', '')
        if new_name:
            parent_folder = attrs.get('parent_folder',
                                      self.instance.parent_folder)
            if Folder.objects.filter(parent_folder=parent_folder,
                                     name=new_name).exists():
                raise ValidationError("There is another folder with the same "
                                      "name in this instance parent folder!")
        return super(FolderBaseSerializer, self).validate(attrs)


class ChildFolderSerializer(FolderBaseSerializer):
    class Meta:
        model = Folder
        exclude = ('owner', 'parent_folder')


class ParentFolderSerializer(FolderBaseSerializer):
    """Serializer for parent folder objects"""

    child_folders = serializers.SerializerMethodField('_get_children_folders')

    def _get_children_folders(self, obj):
        serializer = ChildFolderSerializer(
            obj.get_children_folders(), many=True
        )
        return serializer.data

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder', 'child_folders')
