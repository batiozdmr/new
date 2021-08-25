from django.contrib import admin

# Register your models here.
from apps.content.models import *

admin.site.register(Announcement)
admin.site.register(PostCreate)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(ForumCategory)
admin.site.register(Forum)
admin.site.register(ForumAnswer)
admin.site.register(Event)



