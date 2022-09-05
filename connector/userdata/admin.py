from django.contrib import admin
from .models import *


@admin.register(UserPosting)
class UserPostingAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'uploaded_at', 'image')


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')


@admin.register(FollowAccount)
class FollowAccountAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user',)
