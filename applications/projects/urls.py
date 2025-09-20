from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, LayerGroupViewSet, LayerViewSet, filter_groups_by_project

# Create router and register viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'layer-groups', LayerGroupViewSet)
router.register(r'layers', LayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # AJAX endpoint for admin interface
    path('admin/layergroup/filter-by-project/', filter_groups_by_project, name='filter_groups_by_project'),
]
