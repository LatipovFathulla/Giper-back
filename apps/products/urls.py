from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryList, ProductByCategory, ProductDetailBySlug, AllProductsView, RatingCreate, \
    ProductFilterView, CategoryBrandListView, USAAllProductsView

app_name = "products"
router = DefaultRouter()
# router.register('product_filter', ProductFilterView, basename='produc_filter')
router.register('api/products', AllProductsView, 'products')
router.register('api/product-usa', USAAllProductsView, 'products-usa')
# router.register('api/products/filter', ProductInventoryView, 'products-filter')

urlpatterns = [
    path("category/all/", CategoryList.as_view()),
    path("category/<str:slug>/", ProductByCategory.as_view()),
    path("product-detail/<int:pk>/", ProductDetailBySlug.as_view()),
    # path("api/products/filter/<int:pk>/", ProductInventoryAPIView.as_view()),
    path('ratings/', RatingCreate.as_view(), name='rating-create'),
    path('product_filter/', ProductFilterView.as_view(), name='ProductInventory-list'),
    path('categories-filter/<int:category_id>/', CategoryBrandListView.as_view()),

]
urlpatterns += router.urls
