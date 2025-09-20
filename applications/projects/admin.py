from django.contrib import admin
from django import forms
from django.db import models
from .models import Project, LayerGroup, Layer, DefaultLayer


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


@admin.register(LayerGroup)
class LayerGroupAdmin(admin.ModelAdmin):
    """
    Admin interface for LayerGroup model
    """
    list_display = ['nombre', 'proyecto', 'parent_group', 'orden', 'fold_state']
    list_filter = ['proyecto', 'fold_state', 'parent_group']
    search_fields = ['nombre', 'proyecto__nombre_corto']
    list_editable = ['orden']

    fieldsets = (
        ('Basic Information', {
            'fields': ('proyecto', 'nombre', 'parent_group')
        }),
        ('Display Configuration', {
            'fields': ('orden', 'fold_state')
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
        """
        Override full_clean to handle dynamic grupo field validation
        """
        # Temporarily expand the grupo queryset to include all groups
        # This prevents Django from rejecting dynamically loaded options
        if 'grupo' in self.data and self.data['grupo']:
            try:
                grupo_id = int(self.data['grupo'])
                # Ensure the selected group is in the queryset
                if not self.fields['grupo'].queryset.filter(pk=grupo_id).exists():
                    self.fields['grupo'].queryset = LayerGroup.objects.filter(
                        models.Q(pk=grupo_id) | models.Q(pk__in=self.fields['grupo'].queryset)
                    )
            except (ValueError, TypeError):
                pass
        
        super().full_clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing existing layer, set the project field
        if self.instance and self.instance.pk and self.instance.grupo:
            self.fields['proyecto'].initial = self.instance.grupo.proyecto
            # Filter groups by the layer's project
            self.fields['grupo'].queryset = LayerGroup.objects.filter(
                proyecto=self.instance.grupo.proyecto
            ).select_related('proyecto', 'parent_group')
        else:
            # For new layers, show all groups to avoid validation issues
            # The JavaScript will filter them dynamically
            self.fields['grupo'].queryset = LayerGroup.objects.all().select_related('proyecto', 'parent_group')

        # Add CSS classes and help text
        self.fields['grupo'].widget.attrs.update({
            'id': 'id_grupo',
            'class': 'grupo-selector'
        })
        self.fields['grupo'].help_text = "Seleccione el grupo para esta capa (organizado por proyecto)"

        # Enhance group display with hierarchical names
        if self.fields['grupo'].queryset.exists():
            choices = []
            for group in self.fields['grupo'].queryset:
                if group.parent_group:
                    display_name = f"{group.parent_group.nombre} → {group.nombre}"
                else:
                    display_name = group.nombre
                choices.append((group.pk, display_name))
            self.fields['grupo'].choices = [('', '---------')] + choices

    def clean_grupo(self):
        """
        Custom validation for grupo field that allows dynamically loaded options
        """
        grupo_id = self.data.get('grupo')  # Get raw form data
        
        if not grupo_id:
            raise forms.ValidationError('Debe seleccionar un grupo para la capa.')
        
        try:
            # Validate that the grupo exists and get the object
            grupo = LayerGroup.objects.get(pk=grupo_id)
            return grupo
        except (ValueError, LayerGroup.DoesNotExist):
            raise forms.ValidationError('Escoja una opción válida. Esa opción no está entre las disponibles.')
    
    def clean(self):
        """
        Custom validation that handles the proyecto field properly
        """
        cleaned_data = super().clean()

        # Get the values
        proyecto = cleaned_data.get('proyecto')
        grupo = cleaned_data.get('grupo')

        # If proyecto is provided and grupo exists, validate the relationship
        if proyecto and grupo and grupo.proyecto != proyecto:
            raise forms.ValidationError({
                'grupo': f'El grupo seleccionado no pertenece al proyecto "{proyecto.nombre_corto}".'
            })

        # IMPORTANT: Remove proyecto from cleaned_data since it's not a model field
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


@admin.register(DefaultLayer)
class DefaultLayerAdmin(admin.ModelAdmin):
    """
    Admin interface for DefaultLayer model
    """
    list_display = ['proyecto', 'layer', 'visible_inicial']
    list_filter = ['proyecto', 'visible_inicial']
    search_fields = ['proyecto__nombre_corto', 'layer__nombre_display']
    list_editable = ['visible_inicial']

    fieldsets = (
        ('Configuration', {
            'fields': ('proyecto', 'layer', 'visible_inicial')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
