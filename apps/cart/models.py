from django.db import models
from apps.products.models import NewProductModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name=_('user'))
    product = models.ForeignKey(NewProductModel, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    total = models.CharField(max_length=250, verbose_name=_('total'))
    cart_status = models.BooleanField(verbose_name=_('cart_status'), default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    # def total_price(self):
    #     return self.total



    def __str__(self):
        return str(self.product.title_en)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


