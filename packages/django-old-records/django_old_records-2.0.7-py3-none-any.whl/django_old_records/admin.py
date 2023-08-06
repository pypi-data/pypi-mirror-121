from django.contrib import admin
from django_old_records.models import ModelConfig, FieldConfig

class FieldConfigInline(admin.TabularInline):
    model = FieldConfig

class ModelConfigAdmin(admin.ModelAdmin):
    inlines = [FieldConfigInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content_type')

admin.site.register(ModelConfig, ModelConfigAdmin)
