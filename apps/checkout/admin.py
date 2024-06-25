from django.contrib import admin
from .models import Checkout


@admin.register(Checkout)
class CheckoutModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'PAY_STATUS', 'created_at']
