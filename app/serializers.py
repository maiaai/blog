from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app.models import User, Post, Topic


class UserPostSerializer(serializers.ModelSerializer):
    topic = serializers.HyperlinkedIdentityField(view_name='topic-detail')

    class Meta:
        model = Post
        fields = ('title', 'topic', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    posts = SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'posts', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request', None)

    def get_posts(self, obj):
        return UserPostSerializer(obj.get_user_posts(), many=True, context={'request': self.request}).data

    def validate_email(self, email):
        user = User.objects.filter(email=email).exists()
        if user:
            raise serializers.ValidationError("User with email {} already exists.".format(email))
        return email

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="post-detail")

    class Meta:
        model = Post
        fields = ('url', 'topic', 'user', 'title', 'content', 'status')
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request', None)
        self.user = self.request.user

    def create(self, validated_data):
        data = validated_data
        data['user'] = self.user
        post = Post.objects.create(**data)
        return post


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="topic-detail")
    name = serializers.CharField(max_length=128)

    class Meta:
        model = Topic
        fields = ('url', 'name', )

    def validate_name(self, name):
        topic = Topic.objects.filter(name=name).exists()
        if topic:
            raise serializers.ValidationError("Topic with name {} already exists.".format(name))
        return name
