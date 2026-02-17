from django.shortcuts import render
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import DptoQueries, DptoAmenazas
from .serializers import dptoQueriesSerializer, dptoDangerSerializer

class dptoQuery(ListAPIView):
    """
    API endpoint for retrieving biodiversity data charts by department.
    
    Returns biodiversity occurrence data and statistics for a specific
    Colombian department identified by its code.
    """
    serializer_class = dptoQueriesSerializer

    @swagger_auto_schema(
        operation_description="Get biodiversity chart data for a specific department",
        operation_summary="Department Biodiversity Charts",
        tags=['Department'],
        manual_parameters=[
            openapi.Parameter(
                'kid',
                openapi.IN_PATH,
                description="Department code (e.g., '05' for Antioquia)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Department biodiversity data retrieved successfully",
                schema=dptoQueriesSerializer(many=True)
            ),
            404: openapi.Response(
                description="Department not found"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve biodiversity chart data for a department.
        
        Returns occurrence records and biodiversity statistics
        for the specified department code.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        kid = self.kwargs['kid']
        return DptoQueries.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')


class dptoDanger(ListAPIView):
    """
    API endpoint for retrieving threat/danger data by department.
    
    Returns information about threatened species and conservation
    status for a specific Colombian department.
    """
    serializer_class = dptoDangerSerializer

    @swagger_auto_schema(
        operation_description="Get threat/danger data for a specific department",
        operation_summary="Department Threat Analysis",
        tags=['Department'],
        manual_parameters=[
            openapi.Parameter(
                'kid',
                openapi.IN_PATH,
                description="Department code (e.g., '05' for Antioquia)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Department threat data retrieved successfully",
                schema=dptoDangerSerializer(many=True)
            ),
            404: openapi.Response(
                description="Department not found"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve threat/danger data for a department.
        
        Returns information about threatened species, conservation
        status, and biodiversity risks for the specified department.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        kid = self.kwargs['kid']
        return DptoAmenazas.objects.filter(codigo=kid).exclude(tipo__isnull=True)
