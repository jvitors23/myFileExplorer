from explorer import serializers
from explorer.permissions import ManageOwnObjects
from explorer.models import Folder
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
