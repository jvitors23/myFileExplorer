import os

from rest_framework import serializers

from explorer.models import Folder, File
from rest_framework.exceptions import PermissionDenied, ValidationError


def _get_invalid_character(string: str) -> set:
    return {c for c in string if not c.isalnum()}


class BaseSerializerMixin:

    def validate_name(self, name):
        invalid_characters = _get_invalid_character(name)
        if invalid_characters:
            raise serializers.ValidationError(
                f'Name can\'t have {invalid_characters}'
            )
        return name

    def validate_parent_folder(self, parent_folder):
        if parent_folder.owner != self.context['request'].user:
            # User can't use another user folder
            raise PermissionDenied()
        return parent_folder


class FolderBaseSerializer(serializers.ModelSerializer, BaseSerializerMixin):

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def validate(self, attrs):
        attrs = super(FolderBaseSerializer, self).validate(attrs)
        name = attrs.get('name', '')
        if name:
            old_parent_folder = self.instance and self.instance.parent_folder
            parent_folder = attrs.get('parent_folder') or old_parent_folder
            if Folder.objects.filter(parent_folder=parent_folder,
                                     name=name).exists():
                raise ValidationError("There is another folder with the same "
                                      "name in this parent folder!")
        attrs['owner'] = self.context['request'].user
        return attrs


class ChildFolderSerializer(FolderBaseSerializer):
    class Meta:
        model = Folder
        exclude = ('owner', 'parent_folder')


class FileBaseSerializer(serializers.ModelSerializer, BaseSerializerMixin):
    file = serializers.FileField(max_length=30)

    class Meta:
        model = File
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder', 'file')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at', 'name')
        extra_kwargs = {'file': {'required': True}}

    def validate(self, attrs):
        attrs = super(FileBaseSerializer, self).validate(attrs)
        if attrs['file']:
            filename = attrs['file'].name
            name, extension = os.path.splitext(filename)
            self.validate_name(name)
            old_parent_folder = self.instance and self.instance.parent_folder
            parent_folder = attrs.get('parent_folder') or old_parent_folder
            if File.objects.filter(parent_folder=parent_folder,
                                   name=name).exists():
                raise ValidationError("There is another file with the same "
                                      "name in this parent folder!")
            attrs['name'] = f'{name}{extension}'
        attrs['owner'] = self.context['request'].user
        return attrs


class ChildFileSerializer(FileBaseSerializer):
    size = serializers.SerializerMethodField('_get_file_size')

    def _get_file_size(self, obj):
        return obj.file.size

    class Meta:
        model = File
        exclude = ('owner', 'parent_folder')


class ParentFolderSerializer(FolderBaseSerializer):
    """Serializer for parent folder objects"""

    child_folders = serializers.SerializerMethodField('_get_children_folders')
    child_files = serializers.SerializerMethodField('_get_children_files')

    def _get_children_folders(self, obj):
        serializer = ChildFolderSerializer(
            obj.get_children_folders(), many=True
        )
        return serializer.data

    def _get_children_files(self, obj):
        serializer = ChildFileSerializer(
            obj.get_children_files(), many=True
        )
        return serializer.data

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder', 'child_folders',
                  'child_files'
                  )
