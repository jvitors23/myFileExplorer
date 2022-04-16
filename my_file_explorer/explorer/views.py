from explorer import serializers
from explorer.permissions import ManageOwnObjects
from explorer.models import Folder
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ListFolderAPIView(generics.RetrieveAPIView):

    queryset = Folder.objects.all()
    serializer_class = serializers.ParentFolderSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)


class ManageFolderAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = serializers.FolderBaseSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)


class CreateFolderAPIView(generics.CreateAPIView):
    serializer_class = serializers.FolderBaseSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({'owner': request.user})
        parent_folder = serializer.validated_data.get('parent_folder')
        if parent_folder.owner != self.request.user:
            # User can't use another user folder
            raise PermissionDenied()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)
