from django.urls import path

from apps.search.views import SearchProductInventory

urlpatterns = [
    path("api/", SearchProductInventory.as_view()),
]
