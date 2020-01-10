from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.signup_url = reverse("user-list")
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'shititit',
            'is_organisation': True,
            'address': 'Some city, state',
            'contact_detail': 'some@email.com'
        }

    def test_signup_with_incorrect_fields(self):
        data = {'title': 'new idea'}
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_optional_fields(self):
        data = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'email.email1@gmail.com',
            'password': 'shititit',
            'is_organisation': True,
            'address': 'Some city, state',
            'contact_detail': 'some@email.com'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_correct_fields(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_already_existing_user(self):
        User.objects.create_user(**self.data)
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_already_logged_in_user(self):
        User.objects.create_user(**self.data)
        is_logged_in = self.client.login(
            username=self.data['email'], password=self.data['password']
        )
        self.assertTrue(is_logged_in)
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123',
            'is_organisation': True,
            'address': 'Some city, state',
            'contact_detail': 'some@email.com'
        }
        self.login_data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123'
        }
        self.user = User.objects.create_user(**self.data)

    def test_login_user(self):
        response = self.client.post(
            self.login_url, self.login_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # compare response keys
        self.assertEqual(response.data.keys(), {"auth_token": "XXX"}.keys())

    def test_login_already_logged_in_user(self):
        # If user is already logged in, the same access token will be
        # be returned to the front end
        first_response = self.client.post(
            self.login_url, self.login_data, format='json'
        )
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)

        second_response = self.client.post(
            self.login_url, self.login_data, format='json'
        )
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(first_response.data, second_response.data)
