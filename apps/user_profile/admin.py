from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'first_name', 'phone_number', 'created_at', 'is_superuser', 'is_staff', 'is_active']
    ordering = ['id']
    add_fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 'password', 'is_superuser', 'is_staff', 'mycode',
                'is_active'),
        }),
    )
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 'password', 'is_superuser', 'is_staff', 'mycode',
                'is_active'),
        }),
    )


admin.site.register(User, CustomUserAdmin)