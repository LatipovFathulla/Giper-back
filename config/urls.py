from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Gipermart API By UC-Coding",
        default_version='v1',
        description="Documentation Gipermart",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("outside/", include("apps.outside.urls")),
    path("user/", include("apps.user_profile.urls")),
    path("cart/", include("apps.cart.urls")),
    path("checkout/", include("apps.checkout.urls")),
    # path('', include('apps.payme.urls')),
    path('', include('apps.paycomuz.urls')),
    
    path('dashboard/', include('apps.dashboard_api.urls')),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schem a-redoc'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('product/', include("apps.products.urls")),
    path('search/', include("apps.search.urls"))
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
