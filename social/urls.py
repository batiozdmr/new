from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LoginView

admin.site.site_header = 'T3 Sosyal Yönetimi'
admin.site.index_title = 'T3 Sosyal Yönetimi'
admin.site.site_title = 'T3 Sosyal Yönetim Paneli'

from django.urls import include
from django.urls import path

from django.conf.urls import url
from django.contrib.auth import views

from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from apps.main.views import *
from apps.member_profile.views import *
from apps.content.views import *
app_name = 'social'

urlpatterns = i18n_patterns(

    path('social/super/administrator/user/', admin.site.urls),

    path('rosetta/', include("rosetta.urls")),

    path('', include(('apps.main.urls'), namespace='main')),

    path('', include(('apps.content.urls'), namespace='content')),

    path('search/', user_search, name='user_searchPage'),
    path('account/', include(('apps.member_profile.urls'), namespace='member_profile')),


    path('chat/', include('apps.chat.urls', namespace='chat')),

    path('login/', LoginView.as_view(), name="login_url"),


) + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL,
                                                                            document_root=settings.MEDIA_ROOT)
