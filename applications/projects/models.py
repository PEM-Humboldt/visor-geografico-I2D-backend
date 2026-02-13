from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import RegexValidator


class Project(models.Model):
    """
    Model for managing projects in the Visor I2D platform
    """
    nombre_corto = models.CharField(max_length=50, unique=True, help_text="Short name for URL access")
    nombre = models.CharField(max_length=200, help_text="Full project name")
    logo_pequeno_url = models.URLField(blank=True, null=True, help_text="Small logo URL")
    logo_completo_url = models.URLField(blank=True, null=True, help_text="Complete logo URL")
    nivel_zoom = models.FloatField(default=6.0, help_text="Default zoom level")
    coordenada_central_x = models.FloatField(help_text="Center X coordinate")
    coordenada_central_y = models.FloatField(help_text="Center Y coordinate")
    panel_visible = models.BooleanField(default=True, help_text="Panel visibility on startup")
    base_map_visible = models.CharField(
        max_length=50,
        default='streetmap',
        choices=[
            ('streetmap', 'Street Map'),
            ('cartodb_positron', 'CartoDB Positron'),
            ('otm', 'OpenTopoMap'),
            ('bw', 'Black & White'),
            ('terrain', 'Terrain'),
            ('esri_physical', 'Esri World Physical'),
            ('esri_imagery', 'Esri World Imagery'),
        ],
        help_text="Default visible base map"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.nombre} ({self.nombre_corto})"


class LayerGroup(models.Model):
    """
    Model for layer groups within projects
    """
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='layer_groups')
    nombre = models.CharField(max_length=200, help_text="Group name")
    orden = models.IntegerField(default=0, help_text="Display order")
    fold_state = models.CharField(
        max_length=10,
        choices=[('open', 'Open'), ('close', 'Close')],
        default='close',
        help_text="Initial fold state"
    )
    parent_group = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subgroups',
        help_text="Parent group for subgroups"
    )
    color = models.CharField(
        max_length=7,
        default='#e3e3e3',
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Enter a valid hexadecimal color code (e.g., #FF5733 or #F57)',
                code='invalid_color'
            )
        ],
        help_text='Hexadecimal color code for the layer group (e.g., #FF5733)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'layer_groups'
        verbose_name = 'Layer Group'
        verbose_name_plural = 'Layer Groups'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f"{self.proyecto.nombre_corto} - {self.nombre}"


class Layer(models.Model):
    """
    Model for individual layers
    """
    grupo = models.ForeignKey(LayerGroup, on_delete=models.CASCADE, related_name='layers')
    nombre_geoserver = models.CharField(max_length=200, help_text="GeoServer layer name")
    nombre_display = models.CharField(max_length=200, help_text="Display name in frontend")
    store_geoserver = models.CharField(max_length=200, help_text="GeoServer store name")
    estado_inicial = models.BooleanField(default=False, help_text="Initial visibility state")
    metadata_id = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Metadata ID or external URL"
    )
    orden = models.IntegerField(default=0, help_text="Display order within group")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'layers'
        verbose_name = 'Layer'
        verbose_name_plural = 'Layers'
        ordering = ['orden', 'nombre_display']

    def __str__(self):
        return f"{self.grupo.proyecto.nombre_corto} - {self.nombre_display}"


