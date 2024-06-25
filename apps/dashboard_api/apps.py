from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard_api'
    verbose_name = _('dashboard_api')
