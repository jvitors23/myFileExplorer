from rest_framework import serializers

from explorer.models import Folder


class FolderBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    def validate_name(self, name):
        invalid_character = {c for c in name if not c.isalnum()}
        if invalid_character:
            raise serializers.ValidationError(f'Name can\'t have {invalid_character}')


class ChildFolderSerializer(FolderBaseSerializer):
    class Meta:
        model = Folder
        exclude = ('owner', 'parent_folder')


class ParentFolderSerializer(FolderBaseSerializer):
    """Serializer for parent folder objects"""

    child_folders = serializers.SerializerMethodField('_get_children_folders')

    def _get_children_folders(self, obj):
        serializer = ChildFolderSerializer(obj.get_children_folders(), many=True)
        return serializer.data

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder', 'child_folders')

