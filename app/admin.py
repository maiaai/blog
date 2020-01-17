from django.contrib import admin

from app.models import Author, Post, Topic


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']


class PostAdminSite(admin.ModelAdmin):
    list_display = ['title', 'author', 'topic']
    list_filter = ['title', 'author', 'topic']
    search_fields = ['title', 'content']


class TopicAdminSite(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdminSite)
admin.site.register(Topic, TopicAdminSite)