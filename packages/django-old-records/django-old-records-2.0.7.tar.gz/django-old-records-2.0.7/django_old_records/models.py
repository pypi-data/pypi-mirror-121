from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

def validate_field(value):
    print(value, type(value))

def validate_field_value(value):
    print(value, type(value))

def limit_choices_to():
    query_filter = Q()
    for key in getattr(settings, 'OLD_RECORDS_MODELS', {}):
        for model_name in settings.OLD_RECORDS_MODELS[key]:
            model = apps.get_model(app_label=key, model_name=model_name)
            query_filter |= Q(app_label=model._meta.app_label, model=model._meta.model_name)
    return query_filter

class ModelConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    content_type = models.OneToOneField(
        ContentType,
        limit_choices_to=limit_choices_to,
        on_delete=models.CASCADE,
    )
    max_age = models.DurationField(null=True, blank=True)
    export = models.BooleanField(default=False)
    created_at_field = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.content_type.model_class().__name__

class FieldConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    model_config = models.ForeignKey('ModelConfig', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100, validators=[validate_field])
    value = models.CharField(max_length=100, validators=[validate_field_value])
    max_age = models.DurationField()
