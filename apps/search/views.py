from django.http import HttpResponse
from apps.products.serializers import ProductInventorySearchSerializer
from apps.products.serializers import NewProductSerializer
from apps.products.models import NewProductModel
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.search.documents import NewProductDocument
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response


class SearchProductInventory(ListAPIView):
    queryset = NewProductModel.objects.all()
    serializer_class = NewProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title_en', 'title_ru']
    # productinventory_serializer = ProductInventorySearchSerializer
    # search_document = NewProductDocument
    #
    # def get(self, request, query=None):
    #     try:
    #         q = Q(
    #             "bool",
    #             should=[
    #                 Q("match_phrase_prefix", title_en=query),
    #                 Q("match_phrase_prefix", title_ru=query),
    #                 # Q("match_phrase_prefix", descriptions=query),
    #                 # Q("match_phrase_prefix", brand__name=query),
    #                 Q("match", _id=query),  # id bo'sh maydonni id_ bilan almashtirdik
    #             ],
    #         )
    #         search = self.search_document.search().query(q)
    #         response = search.scan()
    #
    #         serializer = self.productinventory_serializer(response, many=True)
    #         return Response(serializer.data)
    #
    #     except Exception as e:
    #         return HttpResponse(e, status=500)
