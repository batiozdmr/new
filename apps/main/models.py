import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import utc
from django.utils.translation import gettext_lazy as _

from apps.common.fileUpload.userPath import userDirectoryPath
from apps.common.oneTextField import OneTextField

from apps.content.models import Announcement




# Time Counter
from apps.parameter.models import Menu


class TimeCounter(OneTextField):

    summary = models.CharField(max_length=200, blank=True, verbose_name=_('özet'))
    time_counter = models.DateTimeField()
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

    @property
    def time_counter_diff(self):
        # TODO : js ile yapılacak ,bitmedi
        now_2 = timezone.now()
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        now_3 = datetime.datetime.now()
        counter = 0
        print("self.time_counter.year", self.time_counter.year)
        print("self.time_counter.day", self.time_counter.day)
        print("self.time_counter.hour", self.time_counter.hour)
        print("self.time_counter.min", self.time_counter.min)
        print("self.time_counter.second", self.time_counter.second)

        print("self.time_counter :", self.time_counter)
        print("now :", now)
        if self.time_counter > now_2:
            diff = self.time_counter - now_2
            print("diff :", diff)
            print("diff :", diff.days)
            print("diff :", diff.min)
            print("diff :", diff.seconds)
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            hours_2 = diff.total_seconds() / 3600
            hours_3 = hours % 24
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print("counter diff :", days, hours, hours_2, hours_3, minutes, seconds)
            counter = {"days": days, "hours": hours_3, "minutes": minutes, "seconds": seconds}


        else:
            counter = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}

        return counter

    class Meta:
        verbose_name = _('Zaman Sayaç')
        verbose_name_plural = _('Zaman Sayaç')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


# Value Counter
class ValueCounter(OneTextField):

    summary = models.CharField(max_length=200, blank=True, verbose_name=_('Özet'))
    counter_box = models.ManyToManyField("ValueCounterBox", verbose_name=_('Sayaç Değerleri'))
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
        verbose_name = _('Değer Sayaç Section')
        verbose_name_plural = _('Değer Sayaç Section')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


# Value Counter Box
class ValueCounterBox(OneTextField):
    counter = models.CharField(max_length=200, blank=True, verbose_name=_('Sayaç Değeri'))  # integar veya charfield
    icon = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                             verbose_name=_('İcon Görsel'))  # image veya charfield (icon class tag )

    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url

    class Meta:
        verbose_name = _('Değer Sayaç')
        verbose_name_plural = _('Değer Sayaç')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))





class AnnouncementSection(OneTextField):

    summary = models.CharField(max_length=200, blank=True, verbose_name=_('Özet'))
    Announcements = models.ManyToManyField(Announcement,verbose_name=_('Duyurular'))
    icon = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True,
                                    verbose_name=_('İcon Görsel'))



    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url

    class Meta:
        #ordering = ('date',)
        verbose_name = _('Duyuru Bölümü')
        verbose_name_plural = _('Duyuru Bölümü')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))

def menu(request):
    header_menu_list = Menu.objects.order_by('alignment').filter(location='1')
    footer_menu_list = Menu.objects.order_by('alignment').filter(location='2')
    left_menu_list = Menu.objects.order_by('alignment').filter(location='3')
    return {'header_menu_list': header_menu_list, 'footer_menu_list': footer_menu_list, 'about_menu_list': left_menu_list,}


