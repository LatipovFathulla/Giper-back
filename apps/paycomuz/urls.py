from django.urls import path

from apps.paycomuz.views import TestView

urlpatterns = [
    path('paycom/', TestView.as_view())
]