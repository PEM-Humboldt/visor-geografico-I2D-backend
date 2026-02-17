from django.contrib import admin
from django import forms
from django.db import models
from django.utils.html import format_html
from .models import Project, LayerGroup, Layer


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface for Project model
    """
    list_display = ['nombre_corto', 'nombre', 'nivel_zoom', 'panel_visible', 'created_at']
    list_filter = ['panel_visible', 'base_map_visible', 'created_at']
    search_fields = ['nombre_corto', 'nombre']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('nombre_corto', 'nombre')
        }),
        ('Visual Configuration', {
            'fields': ('logo_pequeno_url', 'logo_completo_url')
        }),
        ('Map Configuration', {
            'fields': ('nivel_zoom', 'coordenada_central_x', 'coordenada_central_y', 'base_map_visible')
        }),
        ('UI Configuration', {
            'fields': ('panel_visible',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class LayerGroupAdminForm(forms.ModelForm):
    """
    Custom form with color picker widget
    """
    class Meta:
        model = LayerGroup
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={
                'type': 'color',
                'style': 'width: 100px; height: 40px; cursor: pointer;'
            })
        }


@admin.register(LayerGroup)
class LayerGroupAdmin(admin.ModelAdmin):
    """
    Admin interface for LayerGroup model
    """
    form = LayerGroupAdminForm
    list_display = ['nombre', 'proyecto', 'parent_group', 'orden', 'fold_state', 'color_preview']
    list_filter = ['proyecto', 'fold_state', 'parent_group']
    search_fields = ['nombre', 'proyecto__nombre_corto']
    list_editable = ['orden']

    def color_preview(self, obj):
        """
        Display color preview in list view
        """
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

    fieldsets = (
        ('Basic Information', {
            'fields': ('proyecto', 'nombre', 'parent_group')
        }),
        ('Display Configuration', {
            'fields': ('orden', 'fold_state', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


class LayerAdminForm(forms.ModelForm):
    """
    Custom form for Layer admin with dynamic project-based group filtering
    """
    proyecto = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,  # Not required for saving, only for filtering
        empty_label="Seleccione un proyecto primero",
        help_text="Seleccione el proyecto para filtrar los grupos disponibles",
        widget=forms.Select(attrs={
            'id': 'id_proyecto',
            'class': 'proyecto-selector'
        })
    )

    class Meta:
        model = Layer
        fields = '__all__'

    def full_clean(self):
        if 'grupo' in self.data and self.data['grupo']:
            try:
                grupo_id = int(self.data['grupo'])
                if not self.fields['grupo'].queryset.filter(pk=grupo_id).exists():
                    self.fields['grupo'].queryset = LayerGroup.objects.filter(
                        models.Q(pk=grupo_id) | models.Q(pk__in=self.fields['grupo'].queryset)
                    )
            except (ValueError, TypeError):
                pass
        super().full_clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.grupo:
            self.fields['proyecto'].initial = self.instance.grupo.proyecto
            self.fields['grupo'].queryset = LayerGroup.objects.filter(
                proyecto=self.instance.grupo.proyecto
            )
        else:
            self.fields['grupo'].queryset = LayerGroup.objects.all()

        self.fields['grupo'].widget.attrs.update({
            'id': 'id_grupo',
            'class': 'grupo-selector'
        })

    def clean_grupo(self):
        grupo_id = self.data.get('grupo')
        if not grupo_id:
            raise forms.ValidationError('Debe seleccionar un grupo para la capa.')
        try:
            return LayerGroup.objects.get(pk=grupo_id)
        except (ValueError, LayerGroup.DoesNotExist):
            raise forms.ValidationError('Grupo no válido.')

    def clean(self):
        cleaned_data = super().clean()
        proyecto = cleaned_data.get('proyecto')
        grupo = cleaned_data.get('grupo')

        if proyecto and grupo and grupo.proyecto != proyecto:
            raise forms.ValidationError({
                'grupo': f'El grupo no pertenece al proyecto "{proyecto.nombre_corto}".'
            })

        if 'proyecto' in cleaned_data:
            del cleaned_data['proyecto']

        return cleaned_data


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    """
    Admin interface for Layer model with dynamic project-based group filtering
    """
    form = LayerAdminForm
    list_display = ['nombre_display', 'get_proyecto', 'grupo', 'nombre_geoserver', 'store_geoserver', 'estado_inicial', 'orden']
    list_filter = ['grupo__proyecto', 'grupo', 'estado_inicial', 'store_geoserver']
    search_fields = ['nombre_display', 'nombre_geoserver', 'grupo__nombre', 'grupo__proyecto__nombre_corto']
    list_editable = ['orden', 'estado_inicial']

    def get_proyecto(self, obj):
        """Display project name in list view"""
        return obj.grupo.proyecto.nombre_corto if obj.grupo else '-'
    get_proyecto.short_description = 'Proyecto'
    get_proyecto.admin_order_field = 'grupo__proyecto__nombre_corto'

    fieldsets = (
        ('Selección de Proyecto', {
            'fields': ('proyecto',),
            'description': 'Primero seleccione el proyecto para filtrar los grupos disponibles.'
        }),
        ('Basic Information', {
            'fields': ('grupo', 'nombre_display', 'orden')
        }),
        ('GeoServer Configuration', {
            'fields': ('nombre_geoserver', 'store_geoserver')
        }),
        ('Display Configuration', {
            'fields': ('estado_inicial', 'metadata_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    class Media:
        js = ('projects/admin/js/dynamic_layer_groups.js',)
        css = {
            'all': ('projects/admin/css/dynamic_layer_admin.css',)
        }

    def get_urls(self):
        """Add custom URLs for this admin"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('ajax/filter-groups-by-project/',
                 self.admin_site.admin_view(self.filter_groups_by_project_view),
                 name='projects_layer_filter_groups'),
        ]
        return custom_urls + urls

    def filter_groups_by_project_view(self, request):
        """Admin view wrapper for filtering groups by project"""
        from .views import filter_groups_by_project
        return filter_groups_by_project(request)


