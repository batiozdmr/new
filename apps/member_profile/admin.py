from django.contrib import admin

from .form import SectorApplicationForm
from .models import *
from django.contrib.auth.models import User, Group


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('following_user', 'followed_user')




admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Messages)
admin.site.register(UserGroup)
admin.site.register(SectorCategory)
admin.site.register(Sector)
admin.site.register(Achievement)
admin.site.register(AchievementCategorie)
admin.site.register(GroupRequest)
