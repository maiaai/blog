from django.db import models
from django.contrib.auth.models import AbstractUser

POST_STATUS_CHOICES = [
    ('draft', 'DRAFT'),
    ('published', 'PUBLISHED'),
]


class User(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=252)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + '' + self.last_name

    def get_user_posts(self):
        return Post.objects.filter(user=self)


class Topic(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic')
    title = models.CharField(max_length=252)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=POST_STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
