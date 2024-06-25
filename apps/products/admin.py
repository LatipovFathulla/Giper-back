import pandas as pd
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import TabularInline

from . import models
from .forms import ProductForm, AllMediaAdminForm
from .models import Category, ProductType, ProductAttributeValue, AllMedia, PrColorModel, Brand

admin.site.index_template = 'admin/index.html'
admin.site.app_index_template = 'admin/app_index.html'


class ProductAttributeValuesInline(admin.TabularInline):
    model = models.ProductAttributeValues
    raw_id_fields = ['product']


class NewProductMediaInline(admin.TabularInline):
    model = models.NewMedia
    raw_id_fields = ['product']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cat_image_tag', 'is_active', 'parent']
    search_fields = ['name', 'slug', 'is_active', ]
    list_filter = ['name', 'slug', 'is_active', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

    def cat_image_tag(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" height="60" />'.format(obj.background_image.url))
        else:
            return '-'

    cat_image_tag.short_description = 'Избр'


# @admin.register(models.ProductType)
# class ProductTypeAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']
#     list_filter = ['name']


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


# @admin.register(models.ProductAttributeValues)
# class ProductAttributeValuesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'attributevalues', 'product']
#     search_fields = ['id', 'attributevalues', 'product']
#     list_filter = ['id', 'attributevalues', 'product']


@admin.register(models.ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_attribute', 'attribute_value']
    search_fields = ['id', 'product_attribute', 'attribute_value']
    list_filter = ['id', 'product_attribute', 'attribute_value']


@admin.register(models.ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['id', 'name', 'description']
    list_filter = ['id', 'name', 'description']


#
# @admin.register(models.NewMedia)
# class NewMediaAdmin(admin.ModelAdmin):
#     list_display = ['id']
#     search_fields = ['id']
#     list_filter = ['id']


# @admin.register(models.ProductTypeAttribute)
# class ProductTypeAttributeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product_attribute', 'product_type']
#     search_fields = ['id', 'product_attribute', 'product_type']
#     list_filter = ['id', 'product_attribute', 'product_type']


@admin.register(models.NewProductModel)
class NewProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_ru', 'image_tag', 'price', 'created_at']
    search_fields = ['id', 'title_ru', 'price', 'created_at']
    list_filter = ['id', 'title_ru', 'price', 'created_at']
    exclude = ['user']
    form = ProductForm
    inlines = [NewProductMediaInline]

    def image_tag(self, obj):
        if obj.front_image:
            return format_html('<img src="{}" height="60" />'.format(obj.front_image))
        else:
            return '-'

    image_tag.short_description = 'Избр'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if 'excel_file' in request.FILES:
            # load the Excel file into a pandas dataframe
            df = pd.read_excel(request.FILES['excel_file'])

            # select only the 'name' and 'price' columns, 'attribute_values'
            df = df[['sku', 'title_en', 'title_ru', 'price', 'sale_price', 'installment_plan', 'descriptions', 'weight',
                     'category', 'brand', 'color', 'front_image', 'attribute_values', 'is_active', 'alifshop',
                     'USA_product']]

            # save each row as a new Product object
            for _, row in df.iterrows():
                category_name = row['category']
                category = Category.objects.get(name=category_name)
                brand_names = row['brand'].split(',')
                brands = []
                for name in brand_names:
                    brand, _ = Brand.objects.get_or_create(name=name)
                    brands.append(brand)

                color_names = row['color'].split(',')
                colors = []
                for name in color_names:
                    color, _ = PrColorModel.objects.get_or_create(color=name)
                    colors.append(color)

                attribute_values_list = row['attribute_values'].split(',')
                attribute_values = []
                for value in attribute_values_list:
                    attribute_value, _ = ProductAttributeValue.objects.get_or_create(attribute_value=value)
                    attribute_values.append(attribute_value)

                product = models.NewProductModel(
                    sku=row['sku'],
                    title_en=row['title_en'],
                    title_ru=row['title_ru'],
                    price=row['price'],
                    sale_price=row['sale_price'],
                    installment_plan=row['installment_plan'],
                    descriptions=row['descriptions'],
                    weight=row['weight'],
                    front_image=row['front_image'],
                    is_active=row['is_active'],
                    alifshop=row['alifshop'],
                    USA_product=row['USA_product'],
                    category=category,
                )

                product.save()

                product.attribute_values.set(attribute_values)
                product.color.set(colors)
                product.brand.set(brands)


class AllMediaAdmin(admin.ModelAdmin):
    form = AllMediaAdminForm

    def get_form(self, request, obj=None, **kwargs):
        # Получите форму администратора
        form = super().get_form(request, obj, **kwargs)

        # Заполните поле изображений значениями из базы данных
        images_choices = [(image.id, str(image)) for image in AllMedia.objects.all()]
        form.base_fields['images'].choices = images_choices

        return form


admin.site.register(AllMedia, AllMediaAdmin)


@admin.register(PrColorModel)
class PrColorModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'color', 'created_at']
    search_fields = ['color', ]
