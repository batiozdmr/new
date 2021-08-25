from django.contrib import admin
from .models import *
from translations.admin import TranslatableAdmin, TranslationInline

# Register your models here.
admin.site.register(Menu)
admin.site.register(SubMenu)

admin.site.register(MenuLocation)
admin.site.register(Slider)
admin.site.register(SiteSettings)
admin.site.register(Icons)
admin.site.register(Colors)
admin.site.register(Genders)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Department)
