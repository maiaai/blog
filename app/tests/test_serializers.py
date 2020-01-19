from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from app.models import User, Topic, Post
from app.serializers import TopicSerializer, UserSerializer, PostSerializer


class TestTopicSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test API users
        cls.user = User.objects.create(username='User', email='test@test.com', is_superuser=True, is_staff=True)
        cls.user.set_password("PASS")
        cls.user.save()

    @staticmethod
    def list_url():
        return reverse('topic-list')

    def test_if_no_name_provided_raises_error(self):
        invalid_data = {}
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = TopicSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'name': [u'This field is required.']}
        )

    def test_if_empty_name_provided_raises_error(self):
        invalid_data = {
            'name': ''
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = TopicSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'name': [u'This field may not be blank.']}
        )

    def test_validate_name(self):
        topic = Topic.objects.create(name='Test Topic')
        data = {'name': '{}'.format(topic.name)}
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = TopicSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'name': [u'Topic with name {} already exists.'.format(topic.name)]}
        )


class TestUserSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test API users
        cls.user = User.objects.create(username='User', email='test@test.com', is_superuser=True, is_staff=True)
        cls.user.set_password("PASS")
        cls.user.save()

    @staticmethod
    def list_url():
        return reverse('user-list')

    def test_if_no_user_name_provided_raises_error(self):
        invalid_data = {}
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = TopicSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'name': [u'This field is required.']}
        )

    def test_if_empty_name_provided_raises_error(self):
        invalid_data = {
            'name': '',
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = TopicSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'name': [u'This field may not be blank.']}
        )

    def test_validate_email(self):
        user = User.objects.create(
            first_name='Author',
            last_name='Author',
            email='author@email.com',
        )
        user.set_password('PSW.')
        user.save()
        data = {
            'first_name': '{}'.format(user.first_name),
            'last_name': '{}'.format(user.last_name),
            'email': '{}'.format(user.email),
            'password': user.password
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = UserSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'email': [u'User with email author@email.com already exists.']}
        )


class TestPostSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test API users
        cls.user = User.objects.create(username='User', email='test@test.com', is_superuser=True, is_staff=True)
        cls.user.set_password("PASS")
        cls.user.save()
        cls.topic = Topic.objects.create()

    @staticmethod
    def list_url():
        return reverse('post-list')

    def test_if_no_title_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testserver/api/topics/{}/".format(self.topic.pk),
            "content": "Some content",
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'title': [u'This field is required.']}
        )

    def test_if_empty_title_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testserver/api/topics/{}/".format(self.topic.pk),
            "content": "Some content",
            "title": ""
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'title': [u'This field may not be blank.']}
        )

    def test_if_no_topic_provided_raises_error(self):
        invalid_data = {
            "title": "Some title",
            "content": "Some content",
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'topic': [u'This field is required.']}
        )

    def test_if_empty_topic_provided_raises_error(self):
        invalid_data = {
            "topic": "",
            "content": "Some content",
            "title": "Some title"
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'topic': [u'This field may not be null.']}
        )

    def test_if_bad_topic_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testapi.api/topic/",
            "content": "Some content",
            "title": "Some title"
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'topic': [u'Invalid hyperlink - No URL match.']}
        )

    def test_if_no_content_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testserver/api/topics/{}/".format(self.topic.pk),
            "title": "Some title",
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'content': [u'This field is required.']}
        )

    def test_if_empty_content_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testserver/api/topics/{}/".format(self.topic.pk),
            "content": "",
            "title": "Some title"
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'content': [u'This field may not be blank.']}
        )

    def test_if_empty_status_provided_raises_error(self):
        invalid_data = {
            "topic": "http://testserver/api/topics/{}/".format(self.topic.pk),
            "content": "Some content",
            "title": "Some title",
            "status": ""
        }
        factory = APIRequestFactory()
        request = factory.get(self.list_url())
        request.user = self.user

        serializer = PostSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors, {'status': [u'"" is not a valid choice.']}
        )
