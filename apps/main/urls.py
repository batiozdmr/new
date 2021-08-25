from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

from .views import *
from apps.main.views import *

app_name = "main"
urlpatterns = [

    path('', main, name='mainPage'),
    path('members/', members, name='membersPage'),
    path('members/<str:name>/', groups, name='memberPage'),

]
