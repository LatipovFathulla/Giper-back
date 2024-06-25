from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from .utils.units import Weight, WeightUnits
from ..user_profile.models import User


class Category(MPTTModel):
    name = models.CharField(
        max_length=100, verbose_name=_('name')
    )
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    background_image = models.ImageField(upload_to='category-backgrounds', blank=True, null=True,
                                         verbose_name=_('background_image'))
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_('parent')
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        # unique=True,
        verbose_name=_('name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        # unique=True,
        verbose_name=_('name')
    )
    description = models.TextField(blank=True, verbose_name=_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ProductAttribute')
        verbose_name_plural = _('ProductAttributes')


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name')
    )

    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute",
        verbose_name=_('product_type_attributes')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ProductType')
        verbose_name_plural = _('ProductTypes')


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
        verbose_name=_('product_attribute')
    )
    attribute_value = models.CharField(
        max_length=255,
        verbose_name=_('attribute_value')
    )

    def __str__(self):
        return str(self.attribute_value)

    class Meta:
        verbose_name = _('ProductAttributeValue')
        verbose_name_plural = _('ProductAttributeValue')


class PrColorModel(models.Model):
    color = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет'


class NewProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_products', null=True,
                             verbose_name=_('user'))
    sku = models.CharField(max_length=100, verbose_name=_('sku'))
    title_en = models.CharField(max_length=900, verbose_name=_('title_en'))
    title_ru = models.CharField(max_length=900, verbose_name=_('title_ru'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('category'))
    brand = models.ManyToManyField(
        Brand,
        related_name="new_brand",
        blank=True,
        verbose_name=_('brand')
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="attributes",
        # through="ProductAttributeValues",
        verbose_name=_('attributes'),
        blank=True
    )
    is_recommend = models.BooleanField(default=False, verbose_name=_('is_recommend'), null=True)
    # product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='new_product_type',
    #                                  verbose_name=_('product_type'))
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is_default')
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name=_('price')
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name=_('sale_price')
    )
    installment_plan = models.CharField(max_length=250, verbose_name=_('installment_plan'))
    descriptions = models.TextField(verbose_name=_('descriptions'), max_length=2500, null=True)
    is_on_sale = models.BooleanField(default=False, verbose_name=_('is_on_sale'))
    alifshop = models.BooleanField(default=False, verbose_name=_('alifshop'))
    USA_product = models.BooleanField(default=False, verbose_name=_('USA_product'))
    # weight = MeasurementField(
    #     measurement=Weight,
    #     unit_choices=WeightUnits.CHOICES,  # type: ignore
    #     blank=True,
    #     null=True,
    #     verbose_name=_('weight')
    # )
    weight = models.FloatField(default=0)
    front_image = models.URLField(verbose_name=_('front_image'), max_length=900, null=True, blank=True)
    # color = models.CharField(max_length=100, verbose_name=_('color'), null=True)
    color = models.ManyToManyField(PrColorModel, related_name="new_colors",
                                   blank=True, verbose_name=_('color'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('created_at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated_at')
    )

    PROCESS = "В прогрессе"
    SUCCESS = "Успешно"
    FAILED = "Ошибка"
    DELETED = "Удалено"

    CHOICES = [
        (PROCESS, "Process"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (DELETED, "Deleted"),
    ]

    status = models.CharField(
        max_length=50, choices=CHOICES, default=PROCESS, verbose_name=_('status')
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _('NewProduct')
        verbose_name_plural = _('NewProducts')


class NewMedia(models.Model):
    product = models.ForeignKey(
        NewProductModel,
        on_delete=models.CASCADE,
        related_name="new_media",
        verbose_name=_('media')
    )
    img_url = models.ImageField(upload_to='product/images', verbose_name=_('image_url'))
    alt_text = models.CharField(
        max_length=255,
        verbose_name=_('img_url')
    )
    # is_feature = models.BooleanField(
    #     default=False,
    #     verbose_name=_('alt_text')
    # )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('is_feature')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('created_at')
    )

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')


class Stock(models.Model):
    product = models.OneToOneField(
        NewProductModel,
        related_name="stocks",
        on_delete=models.PROTECT,
        verbose_name=_('product_inventory')
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last_checked')
    )
    units = models.IntegerField(
        default=0,
        verbose_name=_('units')
    )
    units_sold = models.IntegerField(
        default=0,
        verbose_name=_('units_sold')
    )

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stock')


class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('attributevalues')
    )
    product = models.ForeignKey(
        NewProductModel,
        related_name="productattributevaluess",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('product')
    )

    class Meta:
        unique_together = (("attributevalues", "product"),)
        verbose_name = _('ProductAttributeValues')
        verbose_name_plural = _('ProductAttributeValues')

    def __str__(self):
        return str(self.product)


class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('attributevalues')
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('product')
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)
        verbose_name = _('ProductTypeAttribute')
        verbose_name_plural = _('ProductTypeAttribute')

    def __str__(self):
        return str(self.product_attribute)


class Wishlist(models.Model):
    user = models.ForeignKey('user_profile.User', on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(NewProductModel, on_delete=models.CASCADE, verbose_name=_('wishlists'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('date_added'))

    def __str__(self):
        return self.product


class Rating(models.Model):
    product = models.ForeignKey(NewProductModel, on_delete=models.CASCADE, verbose_name=_('ratings'))
    rating = models.PositiveSmallIntegerField(verbose_name=_('rating'))

    def __str__(self):
        return self.rating

    class Meta:
        verbose_name = 'product_all'
        verbose_name_plural = 'product_alls'


class AllMedia(models.Model):
    image = models.FileField(upload_to='all_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Все медиа'
        verbose_name_plural = 'Все медии'

# адрес доставки убрать и сделать null True
# исправить добавления категории
# alifshop добавить для добавлении товаров
# сделать удобным для добавления изображений
# добавить название товаров в списке product-attribute-values
# search users by name
