from django.contrib import admin

from apps.main.models import TimeCounter, ValueCounter, ValueCounterBox,   \
    AnnouncementSection

admin.site.register(TimeCounter)
admin.site.register(ValueCounter)
admin.site.register(ValueCounterBox)

admin.site.register(AnnouncementSection)
