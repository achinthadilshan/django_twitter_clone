from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *

# Unregister Groups
admin.site.unregister(Group)

# Combine profile info with user
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    # display fields on admin page
    fields = ['username']
    inlines = [ProfileInline]


# Unregister initial user
admin.site.unregister(User)

# Register user
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register your models here.
class TweetAdmin(admin.ModelAdmin):
     list_display = ['user', 'body', 'created_at']

admin.site.register(Tweet, TweetAdmin)
