import time

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User
from ads.models import Ad


class AdListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.user1 = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.ad1 = Ad.objects.create(
            title='Test1',
            price=100.99,
            author=self.user,
        )
        time.sleep(0.01)
        self.ad2 = Ad.objects.create(
            title='Test2',
            price=102.99,
            author=self.user1,
        )
        time.sleep(0.01)
        self.ad3 = Ad.objects.create(
            title='Test3',
            price=104.99,
            author=self.user,
        )
        time.sleep(0.01)
        self.ad4 = Ad.objects.create(
            title='Test4',
            price=105.99,
            author=self.user1,
        )
        time.sleep(0.01)
        self.ad5 = Ad.objects.create(
            title='Test5',
            price=106.99,
            author=self.user,
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('ads:ads_list'))

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

    def test_get_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('ads:ads_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        expected_created_at = self.ad2.created_at.isoformat()

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                'count': 5,
                'next': 'http://testserver/ads/?page=2',
                'previous': None,
                'results': [
                    {
                        'author': self.ad5.author.pk,
                        'created_at': self.ad5.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad5.description,
                        'image': None,
                        'price': str(self.ad5.price),
                        'title': self.ad5.title
                    },
                    {
                        'author': self.ad4.author.pk,
                        'created_at': self.ad4.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad4.description,
                        'image': None,
                        'price': str(self.ad4.price),
                        'title': self.ad4.title
                    },
                    {
                        'author': self.ad3.author.pk,
                        'created_at': self.ad3.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad3.description,
                        'image': None,
                        'price': str(self.ad3.price),
                        'title': self.ad3.title
                    },
                    {
                        'author': self.ad2.author.pk,
                        'created_at': self.ad2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad2.description,
                        'image': None,
                        'price': str(self.ad2.price),
                        'title': self.ad2.title
                    },
                ]
            }
        )


class AdCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.ad_data = {
            'title': 'NewOne',
            'price': 0
        }

    def test_not_authenticated(self):
        response = self.client.post(reverse(
            'ads:ads_create'),
            self.ad_data
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

    def test_ad_created_201(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse(
            'ads:ads_create'),
            self.ad_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


class ListMyAdsTestCase(APITestCase):
    def setUp(self):
        self.user_me = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.another_user = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.ad1 = Ad.objects.create(
            title='Test1',
            price=100.99,
            author=self.user_me,
        )
        time.sleep(0.01)
        self.ad2 = Ad.objects.create(
            title='Test2',
            price=102.99,
            author=self.another_user,
        )
        time.sleep(0.01)
        self.ad3 = Ad.objects.create(
            title='Test3',
            price=104.99,
            author=self.user_me,
        )
        time.sleep(0.01)
        self.ad4 = Ad.objects.create(
            title='Test4',
            price=105.99,
            author=self.another_user,
        )
        time.sleep(0.01)
        self.ad5 = Ad.objects.create(
            title='Test5',
            price=106.99,
            author=self.user_me,
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('ads:ads_my_list'))

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

    def test_get_my_list_200(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.get(reverse('ads:ads_my_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'author': self.ad5.author.pk,
                        'created_at': self.ad5.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad5.description,
                        'image': None,
                        'price': str(self.ad5.price),
                        'title': self.ad5.title
                    },
                    {
                        'author': self.ad3.author.pk,
                        'created_at': self.ad3.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad3.description,
                        'image': None,
                        'price': str(self.ad3.price),
                        'title': self.ad3.title
                    },
                    {
                        'author': self.ad1.author.pk,
                        'created_at': self.ad1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'description': self.ad1.description,
                        'image': None,
                        'price': str(self.ad1.price),
                        'title': self.ad1.title
                    },
                ]
            }
        )


class RetrieveAdTestCase(APITestCase):
    def setUp(self):
        self.user_me = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.another_user = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.admin = User.objects.create(
            email='admin@mail.com',
            password='123qwe456rty',
            role='admin'
        )
        self.ad1 = Ad.objects.create(
            title='Test1',
            price=100.99,
            author=self.user_me,
        )
        self.ad2 = Ad.objects.create(
            title='Test2',
            price=102.99,
            author=self.another_user,
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('ads:ad_retrieve', kwargs={'pk': self.ad1.pk}))

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

    def test_get_200_by_any(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.get(reverse('ads:ad_retrieve', kwargs={'pk': self.ad2.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_by_owner(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.get(reverse('ads:ad_retrieve', kwargs={'pk': self.ad1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class PatchAdTestCase(APITestCase):
    def setUp(self):
        self.user_me = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.another_user = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.admin = User.objects.create(
            email='admin@mail.com',
            password='123qwe456rty',
            role='admin'
        )
        self.ad1 = Ad.objects.create(
            title='Test1',
            price=100.99,
            author=self.user_me,
        )
        self.ad2 = Ad.objects.create(
            title='Test2',
            price=102.99,
            author=self.another_user,
        )
        self.data = {
            'title': 'New Title'
        }

    def test_not_authenticated(self):
        response = self.client.patch(reverse('ads:ad_patch', kwargs={'pk': self.ad1.pk}))

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

    def test_no_permission(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.patch(
            reverse('ads:ad_patch', kwargs={'pk': self.ad2.pk}),
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'you are not the owner or administrator of this post'}
        )

    def test_patch_by_owner(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.patch(
            reverse('ads:ad_patch', kwargs={'pk': self.ad1.pk}),
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'author': self.ad1.author.pk,
                'created_at': self.ad1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'description': self.ad1.description,
                'image': None,
                'price': str(self.ad1.price),
                'title': 'New Title'
            }
        )

    def test_patch_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            reverse('ads:ad_patch', kwargs={'pk': self.ad1.pk}),
            self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'author': self.ad1.author.pk,
                'created_at': self.ad1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'description': self.ad1.description,
                'image': None,
                'price': str(self.ad1.price),
                'title': 'New Title'
            }
        )


class DeleteAdTestCase(APITestCase):
    def setUp(self):
        self.user_me = User.objects.create(
            email='test1@mail.com',
            password='123qwe456rty'
        )
        self.another_user = User.objects.create(
            email='test@mail.com',
            password='123qwe456rty'
        )
        self.admin = User.objects.create(
            email='admin@mail.com',
            password='123qwe456rty',
            role='admin'
        )
        self.ad1 = Ad.objects.create(
            title='Test1',
            price=100.99,
            author=self.user_me,
        )
        self.ad2 = Ad.objects.create(
            title='Test2',
            price=102.99,
            author=self.another_user,
        )

    def test_not_authenticated(self):
        response = self.client.delete(reverse('ads:ad_delete', kwargs={'pk': self.ad1.pk}))

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

    def test_no_permission(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.delete(reverse('ads:ad_delete', kwargs={'pk': self.ad2.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'you are not the owner or administrator of this post'}
        )

    def test_delete_by_owner(self):
        self.client.force_authenticate(user=self.user_me)

        response = self.client.delete(reverse('ads:ad_delete', kwargs={'pk': self.ad1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_patch_by_admin(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(reverse('ads:ad_delete', kwargs={'pk': self.ad1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
