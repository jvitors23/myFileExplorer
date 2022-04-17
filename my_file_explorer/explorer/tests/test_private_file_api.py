from rest_framework import status
from explorer.tests.test_public_file_api import BaseFileAPITests
from rest_framework.test import APIClient
from user.views import get_tokens_for_user
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch


class PrivateFolderApiTests(BaseFileAPITests):
    """Test file API private endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(username='jvss',
                                     password='senha123',
                                     first_name='Jose')
        self.tokens = get_tokens_for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.tokens["access"]}'
        )
        self.tmp_file = SimpleUploadedFile(
            'file.jpg', b'file_content', content_type='image/jpg')

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_can_create_file_with_valid_payload(self, mock_save):
        """Test if authenticated user can create file"""
        mock_save.return_value = 'file.jpg'
        payload = {
            'parent_folder': self.user.root_folder.id,
            'file': self.tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'file.jpg')
        self.assertEqual(res.data['size'], self.tmp_file.size)
        mock_save.assert_called_once()  # No file saved!

    def test_user_cant_create_file_with_name_special_char_fails(self):
        """Test if user can't create file invalid payload"""
        tmp_file = SimpleUploadedFile(
            'fil#$%e.jpg', b'file_content', content_type='image/jpg')
        payload = {
            'parent_folder': self.user.root_folder.id,
            'file': tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_file_with_name_greater_than_limit(self):
        """Test if authenticated user can't create file invalid name"""
        tmp_file = SimpleUploadedFile(
            't' * 32, b'file_content', content_type='image/jpg')
        payload = {
            'parent_folder': self.user.root_folder.id,
            'file': tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_file_payload_missing_file_fails(self):
        """Test if authenticated user can't create file missing file"""
        payload = {
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_file_payload_missing_parent_file_fails(self):
        """Test if user can't create file missing parent folder"""
        payload = {
            'file': self.tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_file_notfound_parent_folder_fails(self):
        """Test if user can't create file not found parent folder"""
        payload = {
            'parent_folder': 99999,
            'file': self.tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_create_file_duplicated_name_fails(self, mock_save):
        """Test if user can create file duplicated name
            in the same parent folder fails
        """
        mock_save.return_value = self.tmp_file.name
        self.create_file(name=self.tmp_file.name,
                         parent_folder=self.user.root_folder,
                         owner=self.user,
                         file=self.tmp_file,
                         size=self.tmp_file.size)
        tmp_file = SimpleUploadedFile(
            self.tmp_file.name, b'file_content', content_type='image/jpg')
        payload = {
            'parent_folder': self.user.root_folder.id,
            'file': tmp_file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_can_have_file_same_name_different_parent(self, mock_save):
        """Test if user can create file same name different parent"""
        mock_save.return_value = self.tmp_file.name
        folder = self.create_folder(owner=self.user,
                                    name='test',
                                    parent_folder=self.user.root_folder)
        self.create_file(name=self.tmp_file.name,
                         parent_folder=self.user.root_folder,
                         owner=self.user,
                         file=self.tmp_file,
                         size=self.tmp_file.size)
        file = SimpleUploadedFile(
            self.tmp_file.name, b'file_content', content_type='image/jpg')
        payload = {
            'parent_folder': folder.id,
            'file': file
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_two_users_can_have_files_with_same_name(self, mock_save):
        """Test if two users can  have files with same name"""
        mock_save.return_value = self.tmp_file.name
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        self.create_file(name=self.tmp_file.name,
                         parent_folder=user_2.root_folder,
                         owner=user_2,
                         file=self.tmp_file,
                         size=self.tmp_file.size)

        payload = {
            'parent_folder': self.user.root_folder.id,
            'file': SimpleUploadedFile(self.tmp_file.name,
                                       b'file_content',
                                       content_type='image/jpg')
        }
        res = self.client.post(self.CREATE_FILE_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_authenticated_user_can_edit_own_files(self, mock_save):
        """Test if user can edit own files"""
        mock_save.return_value = self.tmp_file.name
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=self.user,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        payload = {
            'name': 'teste123'
        }
        res = self.client.put(self.file_detail_url(file.id), payload)
        file.refresh_from_db()
        self.assertEqual(res.data['name'], file.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_move_file_that_exists_in_destination_fails(self,
                                                                  mock_save):
        """Test if user can't move file that exists in destination fails"""
        mock_save.return_value = self.tmp_file.name
        self.create_file(name=self.tmp_file.name,
                         parent_folder=self.user.root_folder,
                         owner=self.user,
                         file=self.tmp_file,
                         size=self.tmp_file.size)
        folder = self.create_folder(owner=self.user,
                                    name='test',
                                    parent_folder=self.user.root_folder)
        file_2 = self.create_file(name=self.tmp_file.name,
                                  parent_folder=folder,
                                  owner=self.user,
                                  file=self.tmp_file,
                                  size=self.tmp_file.size)
        payload = {
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.put(self.file_detail_url(file_2.id), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_edit_other_user_files(self, mock_save):
        """Test if user can't edit other user files"""
        mock_save.return_value = self.tmp_file.name
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=user_2,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        payload = {
            'name': 'teste23',
        }
        res = self.client.patch(
            self.file_detail_url(file.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_delete_other_user_folder(self, mock_save):
        """Test if user can't delete other user files"""
        mock_save.return_value = self.tmp_file.name
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=user_2,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        res = self.client.delete(
            self.file_detail_url(file.id)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_cant_retrieve_other_user_file(self, mock_save):
        """Test if user can't retrieve other user file"""
        mock_save.return_value = self.tmp_file.name
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=user_2,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        res = self.client.get(
            self.file_detail_url(file.id)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        mock_save.assert_called_once()  # No file saved!

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_user_can_retrieve_own_file(self, mock_save):
        """Test if user can retrieve own file"""
        mock_save.return_value = self.tmp_file.name
        file = self.create_file(name=self.tmp_file.name,
                                parent_folder=self.user.root_folder,
                                owner=self.user,
                                file=self.tmp_file,
                                size=self.tmp_file.size)
        res = self.client.get(self.file_detail_url(file.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mock_save.assert_called_once()  # No file saved!
