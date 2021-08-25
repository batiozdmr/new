from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf.urls import url
from django.urls import path

from . import views

from .views import *

app_name = "content"
urlpatterns = [

    path('leaderboard/', leaderboard, name='leaderboardPage'),
    path('forum/', forum, name='forumPage'),
    path('calendar/', views.CalendarView.as_view(), name="takvim"),
    path('event/', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

]
