from django.contrib import admin
from django.forms import TextInput
from django_old_records.models import ModelConfig, FieldConfig

class FieldConfigInline(admin.TabularInline):
    model = FieldConfig

class ModelConfigAdmin(admin.ModelAdmin):
    inlines = [FieldConfigInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('content_type')

    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = kwargs.get('widgets', {})
        kwargs['widgets'].update({
            'max_age': TextInput(attrs={'placeholder': '%d %H:%M:%S.%f'})
        })
        return super().get_form(request, obj, **kwargs)

admin.site.register(ModelConfig, ModelConfigAdmin)
