from django.contrib import admin
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


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    """
    Admin interface for Layer model
    """
    list_display = ['nombre_display', 'nombre_geoserver', 'grupo', 'store_geoserver', 'estado_inicial', 'orden']
    list_filter = ['grupo__proyecto', 'grupo', 'estado_inicial', 'store_geoserver']
    search_fields = ['nombre_display', 'nombre_geoserver', 'grupo__nombre']
    list_editable = ['orden', 'estado_inicial']
    
    fieldsets = (
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
