from ckeditor.fields import RichTextField
from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.common.fileUpload.userPath import userDirectoryPath
from apps.common.oneTextField import OneTextField
from django.urls import reverse
from django.contrib.auth.models import User
from apps.member_profile.models import UserProfile
from django.db import models
from datetime import datetime

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.common.fileUpload.userPath import userDirectoryPath

from apps.common.oneTextField import OneTextField
from ckeditor.fields import RichTextField
import calendar


class Announcement(OneTextField):
    keywords = models.TextField(null=True, blank=True, verbose_name=_('Etiketler'))
    summary = models.CharField(max_length=200, blank=True, verbose_name=_('Özet'))
    content = models.TextField(blank=True, verbose_name=_('İçerik'))
    # alignment = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Sıralama'))
    bg_image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                 verbose_name=_('Arkaplan Görsel'))
    icon = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                             verbose_name=_('İcon Görsel'))

    date = models.DateTimeField()

    @property
    def bg_image_url(self):
        if self.bg_image and hasattr(self.bg_image, 'url'):
            return self.bg_image.url

    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url

    class Meta:
        ordering = ('date',)
        verbose_name = _('Duyuru')
        verbose_name_plural = _('Duyuru')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class PostCreate(OneTextField):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name=_('Kullanıcı'))
    content = RichTextField(blank=True, null=True, verbose_name=_('İçerik'))
    image = models.ImageField(upload_to=userDirectoryPath, blank=True, null=True, verbose_name=_('Görsel'))
    video = models.ImageField(blank=True, null=True, verbose_name=_('Video'))
    activity = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Etkinlik'))
    created_at = models.DateTimeField(null=True, blank=True, )

    def date(self):
        time = str(calendar.month_name[self.created_at.month]) + " " + str(self.created_at.day) + "," + str(
            self.created_at.year)
        return time

    class Meta:
        verbose_name = _('Gönderi')
        verbose_name_plural = _('Gönderi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class PostComment(OneTextField):
    post = models.ForeignKey(PostCreate, on_delete=models.PROTECT, verbose_name=_('Gönderi'))
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name=_('Kullanıcı'))
    comment = models.TextField(max_length=150, verbose_name=_('Yorum'))
    sub_comment = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                                    verbose_name=_('Alt Yorum'))

    class Meta:
        verbose_name = _('Gönderi Yorumu')
        verbose_name_plural = _('Gönderi Yorumu')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class PostLike(OneTextField):
    post = models.ForeignKey(PostCreate, on_delete=models.PROTECT, verbose_name=_('Gönderi'))
    users = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name=_('Kullanıcı'))

    class Meta:
        verbose_name = _('Gönderi Beğeni')
        verbose_name_plural = _('Gönderi Beğeni')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))




class ForumAnswer(models.Model):
    answer = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Forum'))

    class Meta:
        verbose_name = _('Cevap')
        verbose_name_plural = _('Cevaplar')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Forum(OneTextField):
    question = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Soru'))
    answer = models.ManyToManyField(ForumAnswer, null=True, blank=True, verbose_name=_('Cevap'))
    answer_size = models.IntegerField(default=0)

    def size(self):
        count = self.answer.all().count()
        return count

    class Meta:
        verbose_name = _('Forum')
        verbose_name_plural = _('Forum')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class ForumCategory(OneTextField):
    image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True, verbose_name=_('Forum Görsel'))
    forums = models.ManyToManyField(Forum, null=True, blank=True, verbose_name=_('Forum'))

    def forum(self):
        forumm=self.forums.all().order_by('-answer_size')
        return forumm

    class Meta:
        verbose_name = _('Forum Kategori')
        verbose_name_plural = _('Forum Kategori')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))



class Event(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Başlık')
    description = models.TextField(null=True, blank=True, verbose_name='İçerik')
    image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                              verbose_name=_('Resim'))
    start_time = models.DateTimeField(verbose_name='Başlangıç Tarihi')
    end_time = models.DateTimeField(verbose_name='Bitiş Tarihi')

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def get_html_url(self):
        url = reverse('content:event_edit', args=(self.id,))
        return f'<a href="{url}"> <img src="{self.image_url}"></a>'

    class Meta:
        verbose_name = _('Aktivite')
        verbose_name_plural = _('Aktivite')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
