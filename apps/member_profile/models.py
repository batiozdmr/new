from ..common.oneTextField.oneField import OneTextField
from django.db import models
from django.contrib.auth.models import User, Group
from apps.common.fileUpload.userPath import userDirectoryPath
from django.utils.translation import gettext_lazy as _
from apps.common.oneTextField import OneTextField
from ckeditor.fields import RichTextField


class AchievementCategorie(OneTextField):
    image = models.ImageField(upload_to=userDirectoryPath, blank=True, null=True, verbose_name=_('Görsel'))
    content = RichTextField(blank=True, null=True, verbose_name='İçerik')

    class Meta:
        verbose_name = _('Başarı Kategori')
        verbose_name_plural = _('Başarı Kategori ')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Achievement(OneTextField):
    image = models.ImageField(upload_to=userDirectoryPath, blank=True, null=True, verbose_name=_(' Görsel'))
    content = RichTextField(blank=True, null=True, verbose_name=' İçerik')
    point = models.IntegerField(blank=True, null=True, verbose_name=' Puan')
    achievement = models.ForeignKey(AchievementCategorie, on_delete=models.PROTECT, verbose_name='Başarı Kategori  ')

    class Meta:
        verbose_name = _('Başarı ')
        verbose_name_plural = _('Başarı ')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class SectorCategory(OneTextField):
    category = models.CharField(max_length=150, blank=True, null=True, verbose_name='Sektör Kategori')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Sektör Kategorisi')
        verbose_name_plural = _('Sektör Kategorisi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Sector(models.Model):
    category = models.ForeignKey(SectorCategory, on_delete=models.PROTECT, related_name='sectorr', blank=True,
                                 verbose_name=_('Sektörler'))
    content = models.CharField(max_length=250, blank=True, null=True, verbose_name='İçerik')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _('Sektör ')
        verbose_name_plural = _('Sektör')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', verbose_name='Kullanıcı')
    image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True, verbose_name=_('Profil Resmi'))
    title = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Başlık'))
    biography = models.TextField(max_length=150, null=True, blank=True, verbose_name=_('Biyografi'))
    school = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Okul'))
    department = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Bölüm'))
    hangouts = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Hangouts'))
    discord = models.URLField(null=True, blank=True, verbose_name=_('Discord'))
    twitter = models.URLField(null=True, blank=True, verbose_name=_('Twitter'))
    instagram = models.URLField(null=True, blank=True, verbose_name=_('Instagram'))
    facebook = models.URLField(null=True, blank=True, verbose_name=_('Facebook'))
    website = models.URLField(null=True, blank=True, verbose_name=_('Web Site'))
    achievement = models.ManyToManyField(Achievement, related_name='achievements', blank=True, verbose_name='Başarı')
    sectors = models.ManyToManyField(SectorCategory, related_name='sector', blank=True, verbose_name=_('Sektörler'))
    total_point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def point(self):
        total = 0
        for count in self.achievement.all():
            total = total + count.point
        return total

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        verbose_name = _('Kullanıcı Profili')
        verbose_name_plural = _('Kullanıcı Profili')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


##değiştir
class UserGroup(OneTextField):
    explanation = models.TextField(max_length=200, null=True, blank=True, verbose_name=_('Açıklama'))
    image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True, verbose_name=_('Grup Resmi'))
    user = models.ManyToManyField(UserProfile, related_name='+', verbose_name=_('Kullanıcı'))

    def all_user(self):
        users = []
        count = 0
        for user in self.user.all():
            if count == 3:
                break
            else:
                users.append(user)
                count = count + 1
        return users

    def count(self):
        count = self.user.all().count() - 3
        if count < 0:
            count = 0
        return count

    class Meta:
        verbose_name = _('Takımlar')
        verbose_name_plural = _('Takımlar')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Follow(models.Model):
    followed_user = models.ForeignKey(UserProfile, verbose_name=_('Takip Edilen', ), related_name='Takip_Edilen',
                                      on_delete=models.PROTECT)
    following_user = models.ForeignKey(UserProfile, verbose_name=_('Takip Eden', ), related_name='Takip_Eden',
                                       on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Takip')
        verbose_name_plural = _('Takip')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', verbose_name='Gönderen')
    message = models.TextField(max_length=1000, blank=True, verbose_name='Mesaj')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    conversation = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', verbose_name='Gönderilen')
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', verbose_name='Kimden')
    is_read = models.BooleanField(default=False, verbose_name='Okundu')

    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['date']

    def __str__(self):
        return self.message

    def get_date_and_hour(self):
        time = self.date.strftime("%I:%M %p")
        date = self.date.strftime("%B %d")
        new_value = "{0} | {1}".format(time, date)
        return new_value

    @staticmethod
    def signed_as_read_message(user, conversation):
        # eğer o anki konuşma ise direk okundu yapıyoruz.
        un_readed_messages = Messages.objects.filter(user=user, conversation=conversation, is_read=False)
        un_readed_messages.update(is_read=True)

    @staticmethod
    def send_message(from_user, to_user, message):
        message = message[:1000]
        current_user_message = Messages(message=message,
                                        user=from_user,
                                        from_user=from_user,
                                        conversation=to_user,
                                        is_read=True)
        current_user_message.save()
        Messages(from_user=from_user,
                 conversation=from_user,
                 user=to_user,
                 message=message).save()

        return current_user_message

    @staticmethod
    def last_message_text_bold_or_normal(last_message, user, index):
        # eğer gelen mesaj karşı taraftan geldiyse ve okunmamışsa bold göstermek için
        if index != 0 and last_message.from_user != user and last_message.is_read == False:
            return "<b style='color:black'>{0}</b>".format(last_message.message)
        return last_message.message

    @staticmethod
    def get_conversations(user):
        conversations = Messages.objects.filter(user=user).values('conversation').annotate(
            last=models.Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            last_message = \
                Messages.objects.filter(user=user, conversation__pk=conversation['conversation']).order_by('-date')[0]
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Messages.objects.filter(user=user, conversation__pk=conversation['conversation'],
                                                  is_read=False).count(),
                'last_message': last_message,
                'last_text': last_message.message
            })

        return users


class GroupRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='+', verbose_name='Kullanıcı Adı')
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Ad')
    surname = models.CharField(max_length=250, null=True, blank=True, verbose_name='Soyad')
    document = models.FileField(upload_to=userDirectoryPath, null=True, blank=True, verbose_name=_('Belge'))
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='+', verbose_name='Grup')
    connection = models.URLField(null=True, blank=True, verbose_name=_('Bağlantı'))

    class Meta:
        verbose_name = _('Grup Talebi')
        verbose_name_plural = _('Grup Talebi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
