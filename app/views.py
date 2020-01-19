from django.db.models import Q
from django.shortcuts import HttpResponse
from rest_framework import viewsets, permissions
from .models import User, Post, Topic
from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer, PostSerializer, TopicSerializer


# Just a single response that can be used for the index page if this Blog had a front-end
def index(request):
    return HttpResponse("Welcome to the Blog")


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_permissions(self):

        # Instantiates and returns the list of permissions that this view requires.

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Override of the basic get_queryset method in order to provide option for search.
    # DRF also provides filter search.
    def get_queryset(self):
        queryset = Post.objects.all()
        qs = self.request.GET.get("q")
        if qs is not None:
            queryset = queryset.filter(
                Q(title__icontains=qs) |
                Q(content__icontains=qs)).distinct()
        return queryset


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
