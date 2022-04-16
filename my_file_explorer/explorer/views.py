from explorer import serializers
from explorer.permissions import ManageOwnObjects, CantManageRootFolder
from explorer.models import Folder, File
from rest_framework import generics, parsers
from rest_framework.permissions import IsAuthenticated


class ListFolderAPIView(generics.RetrieveAPIView):
    """List all elements inside a specific folder"""
    queryset = Folder.objects.all()
    serializer_class = serializers.ParentFolderSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)


class ManageFolderAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Manage folder objects"""
    queryset = Folder.objects.all()
    serializer_class = serializers.FolderBaseSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects,
                          CantManageRootFolder)


class CreateFolderAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FolderBaseSerializer


class ManageFileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Manage file objects"""
    queryset = File.objects.all()
    serializer_class = serializers.FileBaseUpdateDeleteSerializer
    permission_classes = (IsAuthenticated, ManageOwnObjects)
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser,
                      parsers.FileUploadParser)


class CreateFileAPIView(generics.CreateAPIView):
    """Upload a file to specific parent folder"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FileBaseCreateSerializer
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser,
                      parsers.FileUploadParser)
