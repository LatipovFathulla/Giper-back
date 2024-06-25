from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Category, Wishlist, Brand, ProductAttributeValue, Rating, \
    ProductAttribute, NewProductModel, NewMedia
from django.db import models

from .utils.units import Weight


def calculate_rating(product_id):
    ratings = Rating.objects.filter(product=product_id)
    total_ratings = ratings.count()
    if total_ratings == 0:
        return 0
    total_sum = ratings.aggregate(models.Sum('rating'))['rating__sum']
    return int(total_sum) / int(total_ratings)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product', 'date_added')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        depth = 2
        fields = '__all__'
        read_only = True


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductAttributeValueSerializerFiler(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer()

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]
        read_only = True


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.StringRelatedField(source='parent.name')
    parent_id = serializers.StringRelatedField(source='parent.id')

    class Meta:
        model = Category
        fields = ['id', "name", "slug", "description", "background_image", "is_active", 'parent_name', 'parent_id']
        read_only = True


class ProductMediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = NewMedia
        fields = ("img_url", "alt_text")
        read_only_fields = ("img_url", "alt_text")

    def get_img_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.img_url.url)
        return obj.img_url.url


class NewProductSerializer(serializers.ModelSerializer):
    new_media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    category_name = StringRelatedField(source='category.name')
    weight = serializers.SerializerMethodField()
    product_type = serializers.StringRelatedField(source='product_type.name')

    def get_rating(self, obj):
        product_id = obj.id
        return calculate_rating(product_id)

    def get_weight(self, obj):
        weight_obj = obj.weight
        if isinstance(weight_obj, Weight):
            return float(weight_obj.value)
        return 0.0  # or any default value you want

    class Meta:
        model = NewProductModel
        fields = '__all__'


class ProductInventorySearchSerializer(serializers.ModelSerializer):
    # media = ProductMediaSerializer(many=True, read_only=True)
    # new_media = ProductMediaSerializer(many=True, read_only=True)
    new_media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    attributes = ProductAttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = NewProductModel
        # fields = '__all__'
        fields = [
            "id",
            "new_media",
            "title_en",
            "title_ru",
            "sku",
            "front_image",
            "installment_plan",
            "price",
            "descriptions",
            "is_default",
            "is_active",
            "is_on_sale",
            "sale_price",
            "brand",
            'attributes',
            "created_at",
            "updated_at",
        ]

        # read_only_fields = '__all__'
        read_only_fields = ["id", "title", "new_media"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
