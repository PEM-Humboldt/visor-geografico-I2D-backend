from rest_framework import serializers
import re
from .models import Project, LayerGroup, Layer, DefaultLayer


class LayerSerializer(serializers.ModelSerializer):
    """
    Serializer for Layer model
    """
    class Meta:
        model = Layer
        fields = [
            'id', 'nombre_geoserver', 'nombre_display', 'store_geoserver',
            'estado_inicial', 'metadata_id', 'orden'
        ]


class LayerGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for LayerGroup model with nested layers
    """
    layers = LayerSerializer(many=True, read_only=True)
    subgroups = serializers.SerializerMethodField()

    class Meta:
        model = LayerGroup
        fields = [
            'id', 'nombre', 'orden', 'fold_state', 'parent_group',
            'color', 'layers', 'subgroups'
        ]

    def validate_color(self, value):
        """
        Validate hexadecimal color format
        """
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Invalid color format. Use hexadecimal format (e.g., #FF5733 or #F57)'
            )
        return value.upper()  # Normalize to uppercase

    def get_subgroups(self, obj):
        """
        Get subgroups recursively
        """
        subgroups = obj.subgroups.all()
        return LayerGroupSerializer(subgroups, many=True).data


class DefaultLayerSerializer(serializers.ModelSerializer):
    """
    Serializer for DefaultLayer model
    """
    layer = LayerSerializer(read_only=True)

    class Meta:
        model = DefaultLayer
        fields = ['id', 'layer', 'visible_inicial']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model
    """
    class Meta:
        model = Project
        fields = [
            'id', 'nombre_corto', 'nombre', 'logo_pequeno_url', 'logo_completo_url',
            'nivel_zoom', 'coordenada_central_x', 'coordenada_central_y',
            'panel_visible', 'base_map_visible', 'created_at', 'updated_at'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Project model with related data
    """
    layer_groups = LayerGroupSerializer(many=True, read_only=True)
    default_layers = DefaultLayerSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'nombre_corto', 'nombre', 'logo_pequeno_url', 'logo_completo_url',
            'nivel_zoom', 'coordenada_central_x', 'coordenada_central_y',
            'panel_visible', 'base_map_visible', 'layer_groups', 'default_layers',
            'created_at', 'updated_at'
        ]
