from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DjangoOldRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_old_records'
    verbose_name = _("Old Records")
