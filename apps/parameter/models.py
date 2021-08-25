import json

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models
from ..common.oneTextField.oneField import OneTextField
from ..common.mixins.audit import AuditMixin
from ..common.fileUpload.userPath import userDirectoryPath
from ..common.fileUpload.validate import validateFileExtension
from django.contrib.auth.models import Group, User
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from translations.models import Translatable
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class SiteSettings(OneTextField):
    keywords = models.TextField(null=True, verbose_name=_('Etiketler'))
    author = models.CharField(max_length=400, null=True, blank=True, verbose_name=_('Sahip'))
    favicon = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                verbose_name=_('Favicon'))
    header_logo = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                    verbose_name=_('Üst Logo'))
    footer_logo = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                    verbose_name=_('Alt Logo'))
    address = models.TextField(null=True, verbose_name=_('Adres'))
    copyright = models.TextField(null=True, verbose_name=_('Telif"'))
    phone = models.CharField(max_length=400, null=True, blank=True, verbose_name=_('Telefon'))
    facebook = models.URLField(null=True, blank=True, verbose_name=_('Facebook'))
    twitter = models.URLField(null=True, blank=True, verbose_name=_('Twitter'))
    instagram = models.URLField(null=True, blank=True, verbose_name=_('Instagram'))
    telegram = models.URLField(null=True, blank=True, verbose_name=_('Telegram'))
    whatsapp = models.URLField(null=True, blank=True, verbose_name=_('Whatsapp'))
    youtube = models.URLField(null=True, blank=True, verbose_name=_('Youtube'))
    linkedin = models.URLField(null=True, blank=True, verbose_name=_('Linkedin'))
    default_profile_image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                              verbose_name=_('Varsayılan Profil Resmi'))

    @property
    def default_profile_image_url(self):
        if self.default_profile_image and hasattr(self.default_profile_image, 'url'):
            return self.default_profile_image.url
    @property
    def favicon_url(self):
        if self.favicon and hasattr(self.favicon, 'url'):
            return self.favicon.url

    @property
    def header_logo_url(self):
        if self.header_logo and hasattr(self.header_logo, 'url'):
            return self.header_logo.url

    @property
    def footer_logo_url(self):
        if self.footer_logo and hasattr(self.footer_logo, 'url'):
            return self.footer_logo.url

    class Meta:
        ordering = ('text',)
        verbose_name = _('Site Ayarları')
        verbose_name_plural = _('Site Ayarları')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Icons(OneTextField):
    icon = models.CharField(max_length=200, blank=True, verbose_name=_('İcon Kodu'))

    class Meta:
        verbose_name = _('İconlar')
        verbose_name_plural = _('İcon')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class MenuLocation(OneTextField):
    class Meta:
        verbose_name = _('Menü Konumu')
        verbose_name_plural = _('Menü Konumu')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


# Menus
class Menu(OneTextField):
    menu_location = models.ForeignKey(MenuLocation, null=True, blank=True, on_delete=models.PROTECT,
                                      verbose_name=_("Menü Konumu"))
    menu_image = models.ImageField(null=True, blank=True, verbose_name=_("Menü Görsel"))
    menu_icon = models.ForeignKey(Icons, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("Menü İcon"))
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name="URL")
    alignment = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Sıralama'))

    def menuList(self):
        SubMenuList = SubMenu.objects.filter(topMenu=self)
        return SubMenuList

    class Meta:
        verbose_name = _('Menü')
        verbose_name_plural = _('Menü')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class SubMenu(OneTextField):
    topMenu = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name=_("Menü"))

    link = models.CharField(max_length=200, null=True, blank=True, verbose_name="URL")
    alignment = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Sıralama'))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Alt Menü')
        verbose_name_plural = _('Alt Menü')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


# Slider
class Slider(OneTextField):
    # title = models.CharField(max_length=200, blank=True, verbose_name=_('Başlık'))
    link = models.URLField(null=True, blank=True, verbose_name="URL")
    button_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Buton Yazısı")
    summary = models.CharField(max_length=200, blank=True, verbose_name=_('özet'))
    alignment = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Sıralama'))
    bg_image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                 verbose_name=_('Arkaplan Görsel'))
    icon = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                             verbose_name=_('İcon Görsel'))

    @property
    def bg_image_url(self):
        if self.bg_image and hasattr(self.bg_image, 'url'):
            return self.bg_image.url

    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))





class Colors(OneTextField):
    color = models.CharField(max_length=200, blank=True, verbose_name=_('Renk Kodu'))

    class Meta:
        verbose_name = _('Renk')
        verbose_name_plural = _('Renkler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Genders(OneTextField):
    class Meta:
        verbose_name = _('Cinsiyet')
        verbose_name_plural = _('Cinsiyetler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class University(OneTextField):
    class Meta:
        verbose_name = _('Üniversite')
        verbose_name_plural = _('Üniversiteler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Faculty(OneTextField):
    university = models.ForeignKey(University, on_delete=models.PROTECT, verbose_name=_("Üniversite"))

    class Meta:
        verbose_name = _('Fakülte')
        verbose_name_plural = _('Fakülteler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Department(OneTextField):
    university = models.ForeignKey(University, on_delete=models.PROTECT, verbose_name=_("Üniversite"))
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name=_("Fakülte"))

    class Meta:
        verbose_name = _('Bölüm')
        verbose_name_plural = _('Bölümler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
