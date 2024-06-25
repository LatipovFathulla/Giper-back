from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from apps.products.models import NewProductModel

@registry.register_document
class NewProductDocument(Document):

    class Index:
        name = "productinventory"

    class Django:
        model = NewProductModel

        fields = [
            "id",
            "title_en",
            "title_ru",
            "sku",
            "price",
            "descriptions",
            "is_default",
            "is_active",
            "is_on_sale",
            "sale_price",
            "installment_plan",
            "front_image",
            # "weight",
            "created_at",
            "updated_at",
        ]


# @registry.register_document
# class NewProductDocument(Document):
#     class Index:
#         # Name of the Elasticsearch index
#         name = 'new_product'
#         # See Elasticsearch Indices API reference for available settings
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0
#         }
#
#     class Django:
#         model = NewProductModel
#         fields = [
#             'title',
#             'category',
#             'brand',
#             'product_type',
#             'price',
#             'is_on_sale',
#             'weight',
#             'status'
#         ]