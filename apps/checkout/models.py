from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cart.models import CartItem
from apps.paycomuz import Paycom, ChargeStatus
from django.utils.translation import gettext_lazy as _

# from apps.payme.methods.generate_link import GeneratePayLink

User = get_user_model()
paycom = Paycom()

class Checkout(models.Model):
    full_name = models.CharField(max_length=250, verbose_name=_('full_name'))
    phone_number = models.CharField(max_length=100, verbose_name=_('phone_number'))
    region = models.CharField(max_length=100, verbose_name=_('region'))
    town = models.CharField(max_length=100, verbose_name=_('town'))
    address = models.CharField(max_length=200, verbose_name=_('address'))
    comment = models.TextField(verbose_name=_('comment'), null=True, blank=True)
    cart = models.ManyToManyField(CartItem, blank=True, verbose_name=_('cart'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout', null=True, verbose_name=_('user'))
    PAY_STATUS = models.BooleanField(default=False, verbose_name=_('PAY_STATUS'))
    NAXT_STATUS = models.BooleanField(default=False, verbose_name=_('NAXT_STATUS'))
    charge_status = models.CharField(
    max_length=20, 
    choices=ChargeStatus.CHOICES, 
    null=True, 
    blank=True, 
    verbose_name=_('charge_status')
)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    generate_link = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "ORDER ID: {order_id}".format(
            order_id=self.id
        )
        
        
    def all_product(self):
        """
        Returns a queryset of all products in the cart associated with this checkout.
        """
        return self.cart.all().prefetch_related('product').annotate(
            product_title_en=models.F('product__title_en'),
            product_sku=models.F('product__sku'),
            product_price=models.F('product__price'),
        ).values('product_title_en', 'quantity', 'total', 'product_sku', 'product', "product_price")
    
    

    def generate_pay_link(self):
        if self.PAY_STATUS:
            pay_link = paycom.create_initialization(
                order_id=str(self.pk),
                amount=self.amount,
                return_url='https://api.gipermart.uz/paycom/'
            )
            self.generate_link = pay_link
            self.save()

    class Meta:
        verbose_name = _('Checkout')
        verbose_name_plural = _('Checkout')


@receiver(post_save, sender=Checkout)
def checkout_post_save(sender, instance, **kwargs):
    if instance.PAY_STATUS and not instance.generate_link:
        instance.generate_pay_link()