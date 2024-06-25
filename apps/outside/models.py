from django.db import models
from django.utils.safestring import mark_safe
# from apps.user_profile.models import User
from apps.cart.models import User
from apps.products.models import Category, NewProductModel
from django.utils.translation import gettext_lazy as _


class Slider(models.Model):
    url = models.URLField(max_length=250, verbose_name=_('url'))
    images = models.ImageField(upload_to='Slider_img/', default='image.png', verbose_name=_('images'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return self.url

    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')


class Stock(models.Model):
    url = models.URLField(max_length=250, verbose_name=_('url'))
    images = models.ImageField(upload_to='Stock_img/', default='image.png', verbose_name=_('images'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return self.url

    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')


class Brand(models.Model):
    url = models.URLField(max_length=250, verbose_name=_('url'))
    images = models.ImageField(upload_to='Brands_img/', default='image.png', verbose_name=_('images'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('category'))
    product = models.ForeignKey(NewProductModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('product'), related_name='br_product')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return self.url

    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class Add_to_wishlist(models.Model):
    product = models.ForeignKey(NewProductModel, on_delete=models.CASCADE, verbose_name=_('product'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return str(self.id)
