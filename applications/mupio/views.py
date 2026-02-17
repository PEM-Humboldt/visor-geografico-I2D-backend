from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import MpioQueries, MpioAmenazas
from .serializers import mpioQueriesSerializer, mpioDangerSerializer
from applications.mupiopolitico.models import MpioPolitico

class mpioQuery(ListAPIView):
    """
    API endpoint for retrieving biodiversity data charts by municipality.
    
    Returns biodiversity occurrence data and statistics for a specific
    Colombian municipality identified by its code.
    """
    serializer_class = mpioQueriesSerializer

    @swagger_auto_schema(
        operation_description="Get biodiversity chart data for a specific municipality",
        operation_summary="Municipality Biodiversity Charts",
        tags=['Municipality'],
        manual_parameters=[
            openapi.Parameter(
                'kid',
                openapi.IN_PATH,
                description="Municipality code (e.g., '05001' for Medellín)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Municipality biodiversity data retrieved successfully",
                schema=mpioQueriesSerializer(many=True)
            ),
            404: openapi.Response(
                description="Municipality not found"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve biodiversity chart data for a municipality.
        
        Returns occurrence records and biodiversity statistics
        for the specified municipality code.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioQueries.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')


class mpioDanger(ListAPIView):
    """
    API endpoint for retrieving threat/danger data by municipality.
    
    Returns information about threatened species and conservation
    status for a specific Colombian municipality.
    """
    serializer_class = mpioDangerSerializer

    @swagger_auto_schema(
        operation_description="Get threat/danger data for a specific municipality",
        operation_summary="Municipality Threat Analysis",
        tags=['Municipality'],
        manual_parameters=[
            openapi.Parameter(
                'kid',
                openapi.IN_PATH,
                description="Municipality code (e.g., '05001' for Medellín)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Municipality threat data retrieved successfully",
                schema=mpioDangerSerializer(many=True)
            ),
            404: openapi.Response(
                description="Municipality not found"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve threat/danger data for a municipality.
        
        Returns information about threatened species, conservation
        status, and biodiversity risks for the specified municipality.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioAmenazas.objects.filter(codigo=kid).exclude(tipo__isnull=True)


class mpioSearch(ListAPIView):
    """
    API endpoint for searching municipalities by name.
    
    Returns a list of municipalities that match the search term,
    including their coordinates for map navigation.
    """
    
    @swagger_auto_schema(
        operation_description="Search municipalities by name",
        operation_summary="Municipality Search",
        tags=['Municipality'],
        manual_parameters=[
            openapi.Parameter(
                'search_term',
                openapi.IN_PATH,
                description="Search term to find municipalities (e.g., 'buca' for Bucaramanga)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Search results retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "nombre": "BUCARAMANGA",
                            "dpto_nombre": "SANTANDER", 
                            "codigo": "68001",
                            "coord_central": "[-73.1117857645743, 7.15539013995724]"
                        }
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Search municipalities by name.
        
        Returns municipalities that contain the search term in their name,
        along with department name and central coordinates for map navigation.
        """
        search_term = self.kwargs.get('search_term', '')
        
        if not search_term:
            return Response([])
            
        # Search municipalities by name (case insensitive)
        municipalities = MpioPolitico.objects.filter(
            nombre__icontains=search_term
        ).values(
            'nombre', 'dpto_nombre', 'codigo', 'coord_central'
        )[:10]  # Limit to 10 results
        
        return Response(list(municipalities))
