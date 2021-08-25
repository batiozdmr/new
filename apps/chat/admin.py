from django.contrib import admin

# Register your models here.
from apps.chat.models import Message

admin.site.register(Message)
