from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos', null=True, blank=True, verbose_name=_('logo'))
    phonenumbers = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('phone number'))
    site_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('site type'))
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('description'))
    link = models.URLField(null=True, blank=True, verbose_name=_('link'))
    # facebook = models.URLField(null=True, blank=True, verbose_name=_('facebook link'))
    # telegram = models.URLField(null=True, blank=True, verbose_name=_('telegram link'))
    # youtube = models.URLField(null=True, blank=True, verbose_name=_('youtube link'))

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Настройки ссылок'
        verbose_name_plural = 'Настройки ссылок'
