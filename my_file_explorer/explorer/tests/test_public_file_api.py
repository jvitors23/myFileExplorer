from django.contrib.auth import get_user_model
from explorer.models import Folder, File
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


class BaseFileAPITests(TestCase):

    CREATE_FILE_URL = reverse('create_file')

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create_user(**params)

    @staticmethod
    def create_folder(**params):
        return Folder.objects.create(**params)

    @staticmethod
    def create_file(**params):
        return File.objects.create(**params)

    @staticmethod
    def file_detail_url(file_id):
        return reverse('manage_file', args=[file_id])


class PublicFolderApiTests(BaseFileAPITests):
    """Test the files API public endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(username='jvss',
                                     password='senha123',
                                     first_name='Jose')
        self.tmp_file = SimpleUploadedFile(
            'file.jpg', b'file_content', content_type='image/jpg')

    def test_unauthenticated_user_cant_create_file(self):
        """Test if unauthenticated user can't create file"""
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
            'file': self.tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_unauthenticated_user_cant_edit_file(self, mock_save):
        """Test if unauthenticated user can't edit file"""
        mock_save.return_value = self.tmp_file.name
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=self.user,
                                file=self.tmp_file,
                                size=10)
        payload = {
            'name': 'teste23',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.put(self.file_detail_url(file.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.patch(self.file_detail_url(file.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_unauthenticated_user_cant_delete_file(self,  mock_save):
        """Test if unauthenticated user can't delete file"""
        mock_save.return_value = self.tmp_file.name
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=self.user,
                                file=self.tmp_file,
                                size=10)
        res = self.client.delete(self.file_detail_url(file.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_retrieve_file(self, mock_save):
        """Test if unauthenticated user can't retrieve file"""
        mock_save.return_value = self.tmp_file.name
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=self.user,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        res = self.client.get(self.file_detail_url(file.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        mock_save.assert_called_once()  # No file saved!
