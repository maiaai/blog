from django.contrib import admin

from app.models import User, Post, Topic


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    list_filter = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']


class PostAdminSite(admin.ModelAdmin):
    list_display = ['title', 'user', 'topic']
    list_filter = ['title', 'user', 'topic']
    search_fields = ['title', 'content']


class TopicAdminSite(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdminSite)
admin.site.register(Topic, TopicAdminSite)