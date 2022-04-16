from rest_framework import status
from explorer.tests.test_public_folder_api import BaseFolderAPITests
from rest_framework.test import APIClient
from user.views import get_tokens_for_user


class PrivateFolderApiTests(BaseFolderAPITests):
    """Test the folder API private endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(username='jvss',
                                     password='senha123',
                                     first_name='Jose')
        self.tokens = get_tokens_for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.tokens["access"]}'
        )

    def test_user_can_create_folder_with_valid_payload(self):
        """Test if authenticated user can create folder"""
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cant_create_folder_with_name_special_char_fails(self):
        """Test if authenticated user can't create folder invalid payload"""
        payload = {
            'name': 'teste$%@#',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_with_blank_name_fails(self):
        """Test if authenticated user can't create folder blank name fails"""
        payload = {
            'name': '',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_with_name_greater_than_limit(self):
        """Test if authenticated user can't create folder invalid name"""
        payload = {
            'name': 't' * 32,
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_payload_missing_name_fails(self):
        """Test if authenticated user can't create folder missing name"""
        payload = {
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_payload_missing_parent_folder_fails(self):
        """Test if user can't create folder missing parent folder"""
        payload = {
            'name': 'test',
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_notfound_parent_folder_fails(self):
        """Test if user can't create folder not found parent folder"""
        payload = {
            'name': 'test',
            'parent_folder': 9999,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_create_folder_duplicated_name(self):
        """Test if authenticated user can create folder duplicated name
            in the same parent folder
        """
        self.create_folder(owner=self.user,
                           name='test',
                           parent_folder=self.user.root_folder)
        payload = {
            'name': 'test',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_create_folder_valid_payload_success(self):
        """Test if authenticated user can create folder valid payload"""
        payload = {
            'name': 'test',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_have_folder_same_name_different_parent(self):
        """Test if authenticated user can create folder with same name
            but different parent
        """
        folder = self.create_folder(owner=self.user,
                                    name='test',
                                    parent_folder=self.user.root_folder)
        payload = {
            'name': 'test',
            'parent_folder': folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_two_users_can_have_folders_with_same_name(self):
        """Test if two users can  have folders with same name"""
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        self.create_folder(name='test',
                           owner=user_2,
                           parent_folder=user_2.root_folder)
        payload = {
            'name': 'test',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.post(self.CREATE_FOLDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cant_edit_own_folder(self):
        """Test if authenticated user can edit own folder"""
        folder = self.create_folder(name='teste123',
                                    parent_folder=self.user.root_folder,
                                    owner=self.user)
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.put(self.folder_detail_url(folder.id), payload)
        folder.refresh_from_db()
        self.assertEqual(res.data['name'], folder.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cant_move_folder_that_exists_in_destination_fails(self):
        """Test if user can't move folder that exists in destination fails"""
        self.create_folder(name='teste',
                           parent_folder=self.user.root_folder,
                           owner=self.user)

        folder_2 = self.create_folder(name='teste2',
                                      parent_folder=self.user.root_folder,
                                      owner=self.user)
        payload = {
            'name': 'teste',
            'parent_folder': self.user.root_folder.id,
        }
        res = self.client.put(self.folder_detail_url(folder_2.id), payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_edit_root_folder(self):
        """Test if user can't edit root folder"""
        payload = {
            'name': 'teste',
        }
        res = self.client.put(self.folder_detail_url(
            self.user.root_folder.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_edit_other_user_folders(self):
        """Test if user can't edit other user folders"""
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        folder = self.create_folder(name='test',
                                    owner=user_2,
                                    parent_folder=user_2.root_folder)
        payload = {
            'name': 'teste23',
        }
        res = self.client.patch(
            self.folder_detail_url(folder.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_delete_root_folder(self):
        """Test if unauthenticated user can't delete root folder"""
        res = self.client.delete(self.folder_detail_url(
            self.user.root_folder.id)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_delete_other_user_folder(self):
        """Test if user can't delete other user folders"""
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        folder = self.create_folder(name='test',
                                    owner=user_2,
                                    parent_folder=user_2.root_folder)
        res = self.client.delete(
            self.folder_detail_url(folder.id)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_list_other_user_folder(self):
        """Test if unauthenticated user can't retrieve folder"""
        user_2 = self.create_user(username='jvss23',
                                  password='senha123',
                                  first_name='Jose')
        res = self.client.get(
            self.folder_detail_url(user_2.root_folder.id)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list_own_folder(self):
        """Test if unauthenticated user can't list folder objects"""
        self.create_folder(name='test',
                           owner=self.user,
                           parent_folder=self.user.root_folder)
        res = self.client.get(
            self.folder_list_url(self.user.root_folder.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['child_folders']), 1)
