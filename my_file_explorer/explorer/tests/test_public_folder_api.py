from django.contrib.auth import get_user_model
from explorer.models import Folder
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class BaseFolderAPITests(TestCase):

    CREATE_FOLDER_URL = reverse('create_folder')

    @staticmethod
    def create_user(**params):
        return get_user_model().objects.create_user(**params)

    @staticmethod
    def create_folder(**params):
        return Folder.objects.create(**params)

    @staticmethod
    def folder_detail_url(folder_id):
        return reverse('manage_folder', args=[folder_id])

    @staticmethod
    def folder_list_url(folder_id):
        return reverse('list_folder', args=[folder_id])


class PublicFolderApiTests(BaseFolderAPITests):
    """Test the folder API public endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(username='jvss',
                                     password='senha123',
                                     first_name='Jose')

    def test_unauthenticated_user_cant_create_folder(self):
        """Test if unauthenticated user can't create folder"""
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cant_edit_folder(self):
        """Test if unauthenticated user can't edit folder"""
        folder = self.create_folder(name='teste123',
                                    parent_folder=self.user.root_folder,
                                    owner=self.user)
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.put(self.folder_detail_url(folder.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.patch(self.folder_detail_url(folder.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cant_delete_folder(self):
        """Test if unauthenticated user can't delete folder"""
        folder = self.create_folder(name='teste123',
                                    parent_folder=self.user.root_folder,
                                    owner=self.user)
        res = self.client.delete(self.folder_detail_url(folder.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cant_retrieve_folder(self):
        """Test if unauthenticated user can't retrieve folder"""
        folder = self.create_folder(name='teste123',
                                    parent_folder=self.user.root_folder,
                                    owner=self.user)
        res = self.client.get(self.folder_detail_url(folder.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cant_list_folder(self):
        """Test if unauthenticated user can't list folder objects"""
        res = self.client.get(self.folder_list_url(self.user.root_folder.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
