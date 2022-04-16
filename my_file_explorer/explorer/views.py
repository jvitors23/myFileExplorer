from explorer import serializers
from explorer.permissions import ManageOwnObjects
from explorer.models import Folder
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError


class ListFolderAPIView(generics.RetrieveAPIView):

    queryset = Folder.objects.all()
    serializer_class = serializers.ParentFolderSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)


class ManageFolderAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = serializers.FolderBaseSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)

    def perform_update(self, serializer):
        folder = self.get_object()
        if folder.parent_folder is None:
            # User can't edit the root folder
            raise PermissionDenied()

        new_parent_folder = serializer.validated_data.get('parent_folder', '')
        new_name = serializer.validated_data.get('name', '')
        if new_parent_folder:
            if new_parent_folder.owner != self.request.user:
                # User can't use other users folders
                raise PermissionDenied()

        if new_name:
            parent_folder = serializer.validated_data.get('parent_folder',
                                                              folder.parent_folder)
            if Folder.objects.filter(parent_folder=parent_folder, name=new_name).exists():
                raise ValidationError("There is another folder with the same name!")
        return super(ManageFolderAPIView, self).perform_update(serializer)


