from rest_framework import serializers

from explorer.models import Folder


class FolderBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'updated_at',
                  'owner', 'parent_folder')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')


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

