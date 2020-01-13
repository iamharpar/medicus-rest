from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import (
    Address, Organization, MedicalStaff
)

User = get_user_model()


class UserSignupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.second_client = APIClient()
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.signup_url = reverse("user-list")
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'shititit',
            'user_type': 'OR',
            'contact_detail': 'some@email.com',
            'address': {
                'address': 'Some Address or Shit',
                'pincode': '39458',
                'country': 'US',
            },
        }

    def get_user(self):
        return User.objects.get(email=self.data['email'])

    def is_user_created(self):
        return User.objects.filter(email=self.data['email']).exists()

    def create_user(self):
        data = dict(self.data)
        data['address'] = Address.objects.create(**data['address'])
        return User.objects.create_user(**data)

    def test_signup_with_incorrect_fields(self):
        data = {'title': 'new idea'}
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_without_required_fields(self):
        data = dict(self.data)
        data.pop('user_type')  # `user_type` missing
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.is_user_created())

    def test_signup_without_address(self):
        data = dict(self.data)
        data.pop('address')  # removed address
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.is_user_created())

    def test_signup_address_invalid(self):
        data = dict(self.data)
        data['address'].pop('pincode')  # removed pincode from address
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.is_user_created())

    def test_signup_valid(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = self.get_user()
        self.assertTrue(self.is_user_created())
        self.assertTrue(user.is_authenticated and user.is_active)

    def test_signup_existing_user(self):
        self.create_user()
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_logged_in_user(self):
        self.create_user()
        is_logged_in = self.client.login(
            username=self.data['email'], password=self.data['password']
        )
        self.assertTrue(is_logged_in)
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_set_cookie(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cookie_dict = response.client.cookies
        self.assertTrue(cookie_dict['auth_token'])

    def test_signup_authtoken_creation(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['auth_token'])

    def test_signup_authtoken_creation_invalid(self):
        data = dict(self.data)
        data['address'].pop('address')  # invalid address format
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        token = Token.objects.filter(user__email=data['email'])
        self.assertFalse(len(token))

    def test_get_unauthorized_url_after_signup(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.second_client.get(response.data['url'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrganizationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.signup_url = reverse("user-list")
        self.org_name = 'Avenger'
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'shititit',
            'user_type': 'OR',
            'contact_detail': 'some@email.com',
            'address': {
                'address': 'Some Address or Shit',
                'pincode': '39458',
                'country': 'US',
            },
            'organization': {
                'name': 'Avenger',
                'description': 'I am Iron Man !',
            }
        }

    def get_user(self):
        return User.objects.get(email=self.data['email'])

    def is_user_created(self):
        return User.objects.filter(email=self.data['email']).exists()

    def is_organization_created(self):
        return Organization.objects.filter(
            name=self.org_name
        ).exists()

    def create_user(self):
        data = dict(self.data)
        data['address'] = Address.objects.create(**data['address'])
        data['organization'] = Organization.objects.create(
            **data['organization']
        )
        return User.objects.create_user(**data)

    def test_organization_valid_signup(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = self.get_user()
        self.assertTrue(user.is_authenticated and user.is_active)

    def test_organization_creation_valid_signup(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = self.get_user()
        self.assertEqual(user.organization.name, self.org_name)
        self.assertTrue(self.is_organization_created())

    def test_organization_creation_invalid_signup(self):
        # missing `user_type` field
        data = dict(self.data)
        data.pop('user_type')
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.is_user_created())
        self.assertFalse(self.is_organization_created())

    def test_user_creation_invalid_organization(self):
        # missing `name` field from organization
        data = dict(self.data)
        data['organization'].pop('name')
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.is_user_created())
        self.assertFalse(self.is_organization_created())

    def test_organization_exist_login(self):
        self.create_user()
        self.client.login(
            username=self.data['email'], password=self.data['password']
        )
        user = self.get_user()
        self.assertEqual(
            user.organization.name, self.data['organization']['name']
        )

    def test_organization_creation_existing_organization(self):
        self.create_user()
        data = dict(self.data)
        data['email'] = 'some.other_email@email.com'
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123',
            'user_type': 'OR',
            'contact_detail': 'some@email.com',
            'address': {
                'address': 'Some address',
                'pincode': '39458',
                'country': 'US',
            },
            'organization': {
                'name': 'Avenger',
                'description': 'I am Iron Man !',
            }
        }
        self.login_data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123'
        }
        self.user = self.create_user()

    def get_user(self):
        return User.objects.get(email=self.data['email'])

    def create_user(self):
        data = dict(self.data)
        data['address'] = Address.objects.create(**data['address'])
        data['organization'] = Organization.objects.create(
            **data['organization']
        )
        return User.objects.create_user(**data)

    def test_login_user(self):
        response = self.client.post(
            self.login_url, self.login_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['auth_token'])
        user = self.get_user()
        self.assertTrue(user.is_authenticated and user.is_active)

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

    def test_login_with_wrong_credentials(self):
        data = {
            'email': 'email.email1@gmail.com',
            'password': 'wrong password',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cookie_after_login(self):
        response = self.client.post(
            self.login_url, self.login_data, format='json'
        )
        cookie_dict = response.client.cookies
        self.assertTrue(cookie_dict['auth_token'])


class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("user-list")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123',
            'user_type': 'OR',
            'contact_detail': 'some@email.com',
            'address': {
                'address': 'Some address',
                'pincode': '39458',
                'country': 'US',
            },
            'organization': {
                'name': 'Avenger',
                'description': 'I am Iron Man !',
            }
        }
        self.login_data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123'
        }

    def create_user(self):
        data = dict(self.data)
        data['address'] = Address.objects.create(**data['address'])
        data['organization'] = Organization.objects.create(
            **data['organization']
        )
        return User.objects.create_user(**data)

    def test_logout_user_after_signup(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response.data['auth_token']
        )
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_deleted_after_user_logout(self):
        user = self.create_user()
        response = self.client.post(self.login_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response.data['auth_token']
        )
        response = self.client.post(self.logout_url)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_cookie_after_logout(self):
        response = self.client.post(self.signup_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response.data['auth_token']
        )
        response = self.client.post(self.logout_url)
        cookie_header = response.client.cookies['auth_token'].output()
        self.assertIn("expires=Thu, 01 Jan 1970 00:00:00 GMT;", cookie_header)


class UserCheckLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('user-list')
        self.check_url = reverse('check_login')
        self.login_data = {
            'email': 'email.email1@gmail.com',
            'password': 'shititit',
        }
        self.data = {
            'email': 'email.email1@gmail.com',
            'password': 'helloworld123',
            'user_type': 'OR',
            'contact_detail': 'some@email.com',
            'address': {
                'address': 'Some address',
                'pincode': '39458',
                'country': 'US',
            },
            'organization': {
                'name': 'Avenger',
                'description': 'I am Iron Man !',
            }
        }
        self.check_data = {
            'auth_token': '',
        }

    def create_user(self):
        data = dict(self.data)
        data['address'] = Address.objects.create(**data['address'])
        data['organization'] = Organization.objects.create(
            **data['organization']
        )
        return User.objects.create_user(**data)

    def signup_user(self):
        return self.client.post(self.signup_url, self.data, format='json')

    def login_user(self, create_user=False):
        if create_user:
            self.create_user()
        return self.client.post(self.login_url, self.data, format='json')

    def logout_user(self, auth_token):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + auth_token
        )
        return self.client.post(self.logout_url)

    def test_check_user_after_login(self):
        response = self.login_user(create_user=True)
        self.check_data['auth_token'] = response.data['auth_token']
        response = self.client.post(
            self.check_url, self.check_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['logged_in'])

    def test_check_user_after_signup(self):
        response = self.signup_user()
        self.check_data['auth_token'] = response.data['auth_token']
        response = self.client.post(
            self.check_url, self.check_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['logged_in'])

    def test_check_user_after_logout(self):
        response = self.login_user(create_user=True)
        auth_token = response.data['auth_token']
        self.check_data['auth_token'] = auth_token
        self.logout_user(auth_token=auth_token)
        response = self.client.post(
            self.check_url, self.check_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
