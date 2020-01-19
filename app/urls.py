from .views import UserViewSet, PostViewSet, TopicViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


blog_api = DefaultRouter()
blog_api.register(r'users', UserViewSet, 'user')
blog_api.register(r'posts', PostViewSet, 'post')
blog_api.register(r'topics', TopicViewSet, 'topic')

urlpatterns = [
    path('', include(blog_api.urls)),
    path('auth/', include('rest_framework.urls')),
]
