from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

POST_STATUS_CHOICES = [
    ('draft', 'DRAFT'),
    ('published', 'PUBLISHED'),
]

class Author(AbstractUser):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=252)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        verbose_name_plural = 'Authors'


class Topic(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Topics'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic')
    title = models.CharField(max_length=252)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=POST_STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title
