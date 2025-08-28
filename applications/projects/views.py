from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project, LayerGroup, Layer, DefaultLayer
from .serializers import (
    ProjectSerializer, ProjectDetailSerializer, LayerGroupSerializer,
    LayerSerializer, DefaultLayerSerializer
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Project model
    Provides list and retrieve actions for projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        """
        Return detailed serializer for retrieve action
        """
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer

    @action(detail=False, methods=['get'], url_path='by-name/(?P<nombre_corto>[^/.]+)')
    def by_name(self, request, nombre_corto=None):
        """
        Get project by short name (nombre_corto)
        """
        project = get_object_or_404(Project, nombre_corto=nombre_corto)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def layer_groups(self, request, pk=None):
        """
        Get layer groups for a specific project
        """
        project = self.get_object()
        # Get only top-level groups (no parent)
        groups = project.layer_groups.filter(parent_group__isnull=True)
        serializer = LayerGroupSerializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def layers(self, request, pk=None):
        """
        Get all layers for a specific project
        """
        project = self.get_object()
        layers = Layer.objects.filter(grupo__proyecto=project)
        serializer = LayerSerializer(layers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def default_layers(self, request, pk=None):
        """
        Get default layers for a specific project
        """
        project = self.get_object()
        default_layers = project.default_layers.all()
        serializer = DefaultLayerSerializer(default_layers, many=True)
        return Response(serializer.data)


class LayerGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for LayerGroup model
    """
    queryset = LayerGroup.objects.all()
    serializer_class = LayerGroupSerializer

    def get_queryset(self):
        """
        Filter by project if provided
        """
        queryset = LayerGroup.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(proyecto_id=project_id)
        return queryset


class LayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Layer model
    """
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

    def get_queryset(self):
        """
        Filter by project or group if provided
        """
        queryset = Layer.objects.all()
        project_id = self.request.query_params.get('project', None)
        group_id = self.request.query_params.get('group', None)
        
        if project_id is not None:
            queryset = queryset.filter(grupo__proyecto_id=project_id)
        if group_id is not None:
            queryset = queryset.filter(grupo_id=group_id)
            
        return queryset
