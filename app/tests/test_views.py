from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import User, Post, Topic


class TestPostViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test API users
        cls.user = User.objects.create(username='user', email='test@test.com')
        cls.user1 = User.objects.create(username='user1', email='test1@test.com')
        cls.user2 = User.objects.create(username='user2', email='test2@test.com')
        cls.topic = Topic.objects.create(name='Dragons')

        # Create test Posts
        cls.post1 = Post.objects.create(
            title='Drogon',
            user=cls.user1,
            topic=cls.topic
        )
        cls.post2 = Post.objects.create(
            title='Vizerion',
            user=cls.user2,
            topic=cls.topic
        )
        cls.post = Post.objects.create(
            title='Rhaegal',
            user=cls.user,
            topic=cls.topic,
            status='published'
        )

    @staticmethod
    def list_url():
        return reverse('post-list')

    @staticmethod
    def detail_url(pk):
        return reverse('post-detail', kwargs={'pk': pk})

    # GET (list) method
    def test_list_with_non_authenticated_user(self):
        response = self.client.get(self.list_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_items = [
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post1.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user1.pk
                ),
                'title': 'Drogon',
                'content': '',
                'status': 'draft',
            },
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post2.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user2.pk,
                ),
                'title': 'Vizerion',
                'content': '',
                'status': 'draft',
            },
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user.pk,
                ),
                'title': 'Rhaegal',
                'content': '',
                'status': 'published'
            },
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 3)
        actual_items = [dict(item) for item in response.data]
        self.assertEqual(expected_items, actual_items)

    def test_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url())

        expected_items = [
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post1.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user1.pk
                ),
                'title': 'Drogon',
                'content': '',
                'status': 'draft',
            },
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post2.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user2.pk,
                ),
                'title': 'Vizerion',
                'content': '',
                'status': 'draft',
            },
            {
                'url': 'http://testserver/api/posts/{}/'.format(
                    self.post.pk
                ),
                'topic': 'http://testserver/api/topics/{}/'.format(
                    self.topic.pk
                ),
                'user': 'http://testserver/api/users/{}/'.format(
                    self.user.pk,
                ),
                'title': 'Rhaegal',
                'content': '',
                'status': 'published'
            },
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 3)
        actual_items = [dict(item) for item in response.data]
        self.assertEqual(expected_items, actual_items)

    # GET (detail) method
    def test_retrieve_existing_post(self):
        expected_data = {
            'url': 'http://testserver/api/posts/{}/'.format(
                self.post2.pk
            ),
            'topic': 'http://testserver/api/topics/{}/'.format(
                self.topic.pk
            ),
            'user': 'http://testserver/api/users/{}/'.format(
                self.user2.pk
            ),
            'title': 'Vizerion',
            'content': '',
            'status': 'draft'
        }

        # Existing post.
        response = self.client.get(
            self.detail_url(pk=self.post2.pk)
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        actual_data = dict(response.data)
        self.assertDictEqual(expected_data, actual_data)

    def test_retrieve_existing_post_with_authenticated_user(self):
        self.client.force_authenticate(self.user2)

        expected_data = {
            'url': 'http://testserver/api/posts/{}/'.format(
                self.post2.pk
            ),
            'topic': 'http://testserver/api/topics/{}/'.format(
                self.topic.pk
            ),
            'user': 'http://testserver/api/users/{}/'.format(
                self.user2.pk
            ),
            'title': 'Vizerion',
            'content': '',
            'status': 'draft'
        }

        # Existing post.
        response = self.client.get(
            self.detail_url(pk=self.post2.pk)
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        actual_data = dict(response.data)
        self.assertDictEqual(expected_data, actual_data)

    def test_retrieve_non_existing_post(self):
        # Non-existing post
        response = self.client.get(self.detail_url(pk=-1))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({'detail': 'Not found.'}, dict(response.data))

    def test_retrieve_with_random_user(self):
        response = self.client.get(
            self.detail_url(pk=self.post2.pk)
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    # DELETE method
    def test_post_delete_with_random_user(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete(self.detail_url(pk=self.post2.pk))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_delete_with_unauthenticated_user(self):
        response = self.client.delete(self.detail_url(pk=self.post2.pk))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_delete_with_owner(self):
        self.client.force_authenticate(self.user2)
        response = self.client.delete(self.detail_url(pk=self.post2.pk))
        # this means the post was successfully deleted
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    # CREATE method
    def test_post_creation_with_non_authenticated_user(self):
        response = self.client.post(self.list_url())
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_creation_with_authenticated_user(self):
        self.client.force_authenticate(self.user2)
        data = {
            "title": "Some random title",
            "content": "Some random content",
            "topic": "http://testserver/api/topics/1/"
        }
        response = self.client.post(self.list_url(), data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_creation_with_missing_data(self):
        self.client.force_authenticate(self.user2)
        data = {
            "title": "Some random title",
            "content": "Some random content",
        }
        response = self.client.post(self.list_url(), data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    # UPDATE (PUT) method
    def test_post_update_with_non_authenticated_user(self):
        response = self.client.post(self.list_url())
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_update_with_authenticated_user(self):
        self.client.force_authenticate(self.user2)
        data = {
            "title": "Some random title",
            "content": "Some random content",
            "topic": "http://testserver/api/topics/1/"
        }
        response = self.client.post(self.list_url(), data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_update_with_missing_data(self):
        self.client.force_authenticate(self.user2)
        data = {
            "title": "Some random title",
            "content": "Some random content",
        }
        response = self.client.post(self.list_url(), data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class TestUserViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', email='test@test.com', is_staff=True)
        cls.topic = Topic.objects.create(name='Dragons')

        # Create test Post
        cls.post = Post.objects.create(
            title='Rhaegal',
            user=cls.user,
            topic=cls.topic
        )

    @staticmethod
    def list_url():
        return reverse('user-list')

    @staticmethod
    def detail_url(pk):
        return reverse('user-detail', kwargs={'pk': pk})

    # Here can be written same unit tests as unit tests for PostViewSet.
    # Methods: CREATE, UPDATE, DELETE can also be tested.

    # GET (list) method
    def test_list_without_authenticated_user(self):
        response = self.client.get(self.list_url())
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertDictEqual(
            {'detail': 'Authentication credentials were not provided.'},
            dict(response.data),
        )

    def test_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url())
        expected_items = [
            {
                'url': 'http://testserver/api/topics/1/',
                'name': 'Dragons'
            }
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        actual_items = [dict(item) for item in response.data]
        print(actual_items)
        self.assertEqual(expected_items, actual_items)

    # GET (retrieve) method
    def test_retrieve_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        #Existing user
        response = self.client.get(self.detail_url(pk=self.user.pk))
        expected_data = {
                'url': 'http://testserver/api/topics/1/',
                'name': 'Dragons'
            }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        actual_data = dict(response.data)
        self.assertDictEqual(expected_data, actual_data)

        # Non-existing user
        response = self.client.get(self.detail_url(pk=-1))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({'detail': 'Not found.'}, dict(response.data))

    def test_retrieve_without_authenticated_user(self):
        response = self.client.get(self.detail_url(pk=self.user.pk))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertDictEqual(
            {'detail': 'Authentication credentials were not provided.'},
            dict(response.data),
        )


class TestTopicViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', email='test@test.com', is_staff=True)
        cls.topic = Topic.objects.create(name='Dragons')

        # Create test Post
        cls.post = Post.objects.create(
            title='Rhaegal',
            user=cls.user,
            topic=cls.topic
        )

    @staticmethod
    def list_url():
        return reverse('topic-list')

    @staticmethod
    def detail_url(pk):
        return reverse('topic-detail', kwargs={'pk': pk})

    # Here can be written same unit tests as unit tests for PostViewSet.
    # Methods: CREATE, UPDATE, DELETE can also be tested.

    # GET (list) method
    def test_list_without_authenticated_user(self):
        response = self.client.get(self.list_url())
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertDictEqual(
            {'detail': 'Authentication credentials were not provided.'},
            dict(response.data),
        )

    def test_list_with_authenticated_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url())
        expected_items = [
            {
                'url': 'http://testserver/api/topics/1/',
                'name': 'Dragons'
            }
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        actual_items = [dict(item) for item in response.data]
        self.assertEqual(expected_items, actual_items)

    # GET (detail) method
    def test_retrieve_with_authenticated_user(self):
        self.client.force_authenticate(self.user)

        #Existing user
        response = self.client.get(self.detail_url(pk=self.user.pk))
        expected_data = {
                'url': 'http://testserver/api/topics/1/',
                'name': 'Dragons'
            }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        actual_data = dict(response.data)
        self.assertDictEqual(expected_data, actual_data)

        # Non-existing user
        response = self.client.get(self.detail_url(pk=-1))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({'detail': 'Not found.'}, dict(response.data))

    def test_retrieve_without_authenticated_user(self):
        response = self.client.get(self.detail_url(pk=self.user.pk))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertDictEqual(
            {'detail': 'Authentication credentials were not provided.'},
            dict(response.data),
        )
