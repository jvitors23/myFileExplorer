from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('register')
LOGIN_URL = reverse('login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'username': 'jvss',
            'first_name': 'jose',
            'password': 'test123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_invalid_user_fails(self):
        """Test creating user with invalid payload fails"""
        payload = {
            'invalid': 'jvss',
            'first_name': 'jose',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # No name provided
        payload = {
            'username': 'test',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # No username provided
        payload = {
            'first_name': 'jose',
            'password': 'test123'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """Test creating an user that already exists fails"""
        payload = {'username': 'test',
                   'password': 'test123',
                   'first_name': 'jose'
                   }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'username': 'jvss',
                   'first_name': 'jose',
                   'password': 'pw'
                   }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            username=payload['username']).exists()

        self.assertFalse(user_exists)

    def test_user_login(self):
        """Test that user login success with valid credentials"""
        payload = {
            'username': 'jvss',
            'password': 'test123',
            'first_name': 'jose'
        }
        create_user(**payload)
        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_fails_with_invalid_credentials(self):
        """Test that user login fails with invalid credentials"""

        create_user(username='jv', password='test123')
        payload = {
            'username': 'jv@email.com',
            'password': 'wrong'
        }
        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
