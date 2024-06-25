from django.contrib import admin
from .models import Slider, Stock, Brand, Add_to_wishlist


@admin.register(Slider)
class Slideradmin(admin.ModelAdmin):
    """Slider admin"""
    list_display = ("id", "url", "images", "created_at", "updated_at", "image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)


@admin.register(Stock)
class Stockadmin(admin.ModelAdmin):
    """Stock admin"""
    list_display = ("id", "url", "images", "created_at", "updated_at", "image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)


@admin.register(Brand)
class Brandadmin(admin.ModelAdmin):
    """Brand admin"""
    list_display = ("id", "url", "images", "category", "product", "created_at", "updated_at", "image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)

# @admin.register(Add_to_cart)
# class Add_to_cartadmin(admin.ModelAdmin):
#     """Add_to_cart admin"""
#     list_display = ("id","product","user","created_at","updated_at")
#     list_display_links = ("user",)
