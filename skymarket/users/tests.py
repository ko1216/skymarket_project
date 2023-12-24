from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class GetUsersTestCase(APITestCase):

    def setUp(self) -> None:
        self.users_url = 'http://localhost:8000/users/'
        self.default_user = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.admin = User.objects.create(
            email='admin@mail.com',
            password='123qwe456rty',
            role='admin'
        )

    def test_not_authenticated(self):
        response = self.client.get(self.users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                'Authentication credentials were not provided.'
            }
        )

    def test_user_role(self):
        self.client.force_authenticate(user=self.default_user)

        response = self.client.get(self.users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_admin_role(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PostUserTestCase(APITestCase):

    def setUp(self):
        self.users_url = 'http://localhost:8000/users/'
        self.default_user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.new_user = {
            'email': 'test@mail.com',
            'password': '123qwe456rty',
            're_password': '123qwe456rty'
        }
        self.user_email_failed = {
            'email': 'test0@mail.com',
            'password': '123qwe456rty',
            're_password': '123qwe456rty'
        }
        self.user_simple_password = {
            'email': 'test1@mail.com',
            'password': '12345678',
            're_password': '12345678'
        }
        self.user_email_not_valid = {
            'email': 'zxc.zxc',
            'password': '123qwe456rty',
            're_password': '123qwe456rty'
        }
        self.user_password_not_match = {
            'email': 'test@mail.com',
            'password': '123qwe456rt',
            're_password': '123qwe456rty'
        }

    def test_create_201(self):
        response = self.client.post(
            self.users_url,
            self.new_user
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_already_exists(self):
        response = self.client.post(
            self.users_url,
            self.user_email_failed
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'email': ['user with this email already exists.']
            }
        )

    def test_password_is_simple(self):
        response = self.client.post(
            self.users_url,
            self.user_simple_password
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'password': [
                    'This password is too common.',
                    'This password is entirely numeric.'
                ]
            }
        )

    def test_email_not_valid(self):
        response = self.client.post(
            self.users_url,
            self.user_email_not_valid
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'email': [
                    'Enter a valid email address.'
                ]
            }
        )

    def test_not_matching_password(self):
        response = self.client.post(
            self.users_url,
            self.user_password_not_match
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    "The two password fields didn't match."
                ]
            }
        )


class ActivateUserTestCase(APITestCase):
    def setUp(self):
        self.users_url = 'http://localhost:8000/users/'
        self.activation_url = 'http://localhost:8000/users/activation/'
        # self.user_jwt_create = 'http://localhost:8000/jwt/create/'
        self.user = {
            'email': 'test@mail.com',
            'password': '123qwe456rty',
            're_password': '123qwe456rty'
        }
        # self.user_login = {
        #     'email': 'test@mail.com',
        #     'password': '123qwe456rty'
        # }

    def test_activate(self):
        response = self.client.post(
            self.users_url,
            self.user
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(len(mail.outbox), 1)

        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [l for l in email_lines if '/activate/' in l][0]
        uid, token = activation_link.split('/')[-2:]

        data = {
            'uid': uid,
            'token': token
        }
        response = self.client.post(
            self.activation_url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class GetUserMeTestCase(APITestCase):
    def setUp(self):
        self.users_me_url = 'http://127.0.0.1:8000/users/me/'
        self.user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )

    def test_not_authenticated(self):
        response = self.client.get(self.users_me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_get_200(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.users_me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['email'],
            self.user.email
        )


class PutUserMeTestCase(APITestCase):
    def setUp(self):
        self.users_me_url = 'http://127.0.0.1:8000/users/me/'
        self.user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.data = {
            'phone': '+79102003040'
        }

    def test_not_authenticated(self):
        response = self.client.put(self.users_me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_put_200(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            self.users_me_url,
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )


class PatchUserMeTestCase(APITestCase):
    def setUp(self):
        self.users_me_url = 'http://127.0.0.1:8000/users/me/'
        self.user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.data = {
            'phone': '+79102003040'
        }

    def test_not_authenticated(self):
        response = self.client.patch(self.users_me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_put_200(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.users_me_url,
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )


class DeleteUserMeTestCase(APITestCase):
    def setUp(self):
        self.users_me_url = 'http://127.0.0.1:8000/users/me/'
        self.user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )

    def test_not_authenticated(self):
        response = self.client.delete(self.users_me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_put_200(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            self.users_me_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class GetUserIdTestCase(APITestCase):
    def setUp(self):
        self.users_id_url = 'http://127.0.0.1:8000/users/'
        self.user1 = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.user2 = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.user_admin = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty',
            role='admin'
        )

    def test_not_authenticated(self):
        response = self.client.get(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_user_without_perm(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.users_id_url + f'{self.user2.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_get_200(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_with_admin_perm(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.get(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PutUserIdTestCase(APITestCase):
    def setUp(self):
        self.users_id_url = 'http://127.0.0.1:8000/users/'
        self.user1 = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.user2 = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.user_admin = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty',
            role='admin'
        )
        self.data = {
            'phone': '+79102003040'
        }

    def test_not_authenticated(self):
        response = self.client.put(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_user_without_perm(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.put(
            self.users_id_url + f'{self.user2.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_put_200(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.put(
            self.users_id_url + f'{self.user1.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )

    def test_put_with_admin_perm(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.put(
            self.users_id_url + f'{self.user1.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )


class PatchUserIdTestCase(APITestCase):
    def setUp(self):
        self.users_id_url = 'http://127.0.0.1:8000/users/'
        self.user1 = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.user2 = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.user_admin = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty',
            role='admin'
        )
        self.data = {
            'phone': '+79102003040'
        }

    def test_not_authenticated(self):
        response = self.client.patch(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_user_without_perm(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.patch(
            self.users_id_url + f'{self.user2.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_patch_200(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.patch(
            self.users_id_url + f'{self.user1.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )

    def test_patch_with_admin_perm(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.patch(
            self.users_id_url + f'{self.user1.id}/',
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['phone'],
            '+79102003040'
        )


class DeleteUserIdTestCase(APITestCase):
    def setUp(self):
        self.users_id_url = 'http://127.0.0.1:8000/users/'
        self.user1 = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.user2 = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.user_admin = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty',
            role='admin'
        )

    def test_not_authenticated(self):
        response = self.client.delete(self.users_id_url + f'{self.user1.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_user_without_perm(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            self.users_id_url + f'{self.user2.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_204(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            self.users_id_url + f'{self.user1.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_delete_with_admin_perm(self):
        self.client.force_authenticate(user=self.user_admin)

        response = self.client.delete(
            self.users_id_url + f'{self.user1.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SetPasswordTestCase(APITestCase):
    def setUp(self):
        self.password_re_url = 'http://127.0.0.1:8000/users/set_password/'
        self.user = User.objects.create(
            email='test0@mail.com',
            password='123qwe456rty'
        )
        self.user.set_password('123qwe456rty')
        self.user.save()
        self.password = {
            "new_password": "123qwe456rty1",
            "re_new_password": "123qwe456rty1",
            "current_password": "123qwe456rty"
        }
        self.wrong_cur_password = {
            'new_password': '123qwe456rty0',
            're_new_password': '123qwe456rty0',
            'current_password': '123qwe456rt'
        }
        self.pass_not_match = {
            'new_password': '123qwe456rty1',
            're_new_password': '123qwe456rty0',
            'current_password': '123qwe456rty'
        }

    def test_not_authenticated(self):
        response = self.client.post(
            self.password_re_url,
            self.password
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'detail':
                    'Authentication credentials were not provided.'
            }
        )

    def test_set_password_204(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.password_re_url,
            self.password
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_current_pass_not_valid(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.password_re_url,
            self.wrong_cur_password
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'current_password': [
                    'Invalid password.'
                ]
            }
        )

    def test_not_matching_password(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.password_re_url,
            self.pass_not_match
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    "The two password fields didn't match."
                ]
            }
        )


class ResetConfirmPasswordTestCase(APITestCase):
    def setUp(self):
        self.reset_password_url = 'http://localhost:8000/users/reset_password/'
        self.reset_password_confirm = 'http://localhost:8000/users/reset_password_confirm/'
        self.user = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.user_email = {
            'email': 'test@mail.com',
        }
        self.passwords = {
            'new_password': '123qwe456rty1',
            're_new_password': '123qwe456rty1'
        }

    def test_reset_password(self):
        response = self.client.post(
            self.reset_password_url,
            self.user_email
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(len(mail.outbox), 1)

        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [l for l in email_lines if '/confirm/' in l][0]
        uid, token = activation_link.split('/')[-2:]

        data = {
            'uid': uid,
            'token': token
        }
        data.update(self.passwords)
        response = self.client.post(
            self.reset_password_confirm,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
