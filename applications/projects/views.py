from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, LayerGroup, Layer, DefaultLayer
from .serializers import (
    ProjectSerializer, ProjectDetailSerializer, LayerGroupSerializer,
    LayerSerializer, DefaultLayerSerializer
)


@staff_member_required
@require_http_methods(["GET"])
def filter_groups_by_project(request):
    """
    AJAX view to filter layer groups by project for admin interface
    Returns JSON response with groups for the selected project
    """
    # Check if user is staff and has proper permissions
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    # Check if user has permission to view LayerGroup
    if not request.user.has_perm('projects.view_layergroup'):
        return JsonResponse({'error': 'No permission to view layer groups'}, status=403)

    project_id = request.GET.get('project_id')
    grupo_id = request.GET.get('grupo_id')

    # Handle case where we need to find project from grupo (edit case)
    if grupo_id and not project_id:
        try:
            grupo = LayerGroup.objects.select_related('proyecto').get(pk=int(grupo_id))
            return JsonResponse({
                'success': True,
                'project_id': grupo.proyecto.pk,
                'project_name': grupo.proyecto.nombre_corto
            })
        except (ValueError, LayerGroup.DoesNotExist):
            return JsonResponse({'error': 'Invalid grupo_id or grupo not found'}, status=400)

    if not project_id:
        return JsonResponse({'error': 'No project_id provided'}, status=400)

    try:
        # Validate project_id is a valid integer
        project_id = int(project_id)
        project = Project.objects.get(pk=project_id)
        groups = LayerGroup.objects.filter(proyecto=project).select_related('parent_group').order_by('orden', 'nombre')

        # Build hierarchical group data
        groups_data = []
        for group in groups:
            if group.parent_group:
                display_name = f"{group.parent_group.nombre} → {group.nombre}"
            else:
                display_name = group.nombre

            groups_data.append({
                'id': group.pk,
                'nombre': display_name,
                'parent_id': group.parent_group.pk if group.parent_group else None,
                'orden': group.orden
            })

        return JsonResponse({
            'success': True,
            'groups': groups_data,
            'project_name': project.nombre_corto,
            'count': len(groups_data)
        })

    except ValueError:
        return JsonResponse({'error': 'Invalid project_id format'}, status=400)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in filter_groups_by_project: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


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


class LayerGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for LayerGroup model with full CRUD operations
    """
    queryset = LayerGroup.objects.all()
    serializer_class = LayerGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Filter by project if provided
        """
        queryset = LayerGroup.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(proyecto_id=project_id)
        return queryset

    def perform_create(self, serializer):
        """
        Custom create with validation
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom update with validation
        """
        serializer.save()


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
