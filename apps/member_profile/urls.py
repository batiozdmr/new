from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

from .views import *
from apps.member_profile.views import *

app_name = "member_profile"
urlpatterns = [

    path('register/', register, name='registerPage'),
    path('profile/', profile, name='profilePage'),
    path('profile_edit/', profil_edit, name='profileEditPage'),
    path('sector/', sector, name='sectorPage'),
]
