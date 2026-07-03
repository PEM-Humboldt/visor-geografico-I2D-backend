import os
from django.shortcuts import render
import io
import csv
import json
from django.http import HttpResponse, FileResponse
from django.db import connection

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import gbifInfo
from .serializers import gbifInfoSerializer
from .utils import generar_zip

from django.conf import settings

class GbifInfo(ListAPIView):
    """
    API endpoint for retrieving GBIF (Global Biodiversity Information Facility) data.

    This endpoint provides access to biodiversity occurrence records and species
    information from the GBIF database for Colombian biodiversity.
    """
    serializer_class = gbifInfoSerializer

    @swagger_auto_schema(
        operation_description="Retrieve GBIF biodiversity occurrence records",
        operation_summary="Get GBIF Data",
        tags=['GBIF'],
        responses={
            200: openapi.Response(
                description="List of GBIF records retrieved successfully",
                schema=gbifInfoSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve all GBIF biodiversity occurrence records.

        Returns a comprehensive list of biodiversity occurrence data
        including species information, geographic coordinates, and metadata.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return gbifInfo.objects.all()

@swagger_auto_schema(
    method='get',
    operation_description="Download biodiversity data as ZIP file containing CSV files",
    operation_summary="Download GBIF Data (ZIP)",
    tags=['GBIF'],
    manual_parameters=[
        openapi.Parameter(
            'codigo_mpio',
            openapi.IN_QUERY,
            description="Municipality code for filtering data",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'codigo_dpto',
            openapi.IN_QUERY,
            description="Department code for filtering data",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'nombre',
            openapi.IN_QUERY,
            description="Custom name for the downloaded file",
            type=openapi.TYPE_STRING,
            required=False,
            default='descarga_datos'
        )
    ],
    responses={
        200: openapi.Response(
            description="ZIP file containing biodiversity data CSV files",
            schema=openapi.Schema(type=openapi.TYPE_FILE)
        ),
        400: openapi.Response(
            description="Missing required parameters",
            examples={
                "application/json": {
                    "error": "Debe proporcionar codigo_mpio o codigo_dpto"
                }
            }
        )
    }
)
@api_view(['GET'])
def descargarzip(request):
    """
    Download biodiversity data as ZIP file.

    Downloads GBIF occurrence records and species lists filtered by
    municipality or department code. Returns a ZIP file containing
    two CSV files: registros.csv and lista_especies.csv.

    Either codigo_mpio or codigo_dpto must be provided.

    SECURITY: SQL injection protection with input validation.
    """
    import re

    # Validate input parameters
    codigo_mpio = request.GET.get('codigo_mpio')
    codigo_dpto = request.GET.get('codigo_dpto')

    if not codigo_mpio and not codigo_dpto:
        return Response(
            {'error': 'Debe proporcionar codigo_mpio o codigo_dpto'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate code format to prevent SQL injection
    if codigo_mpio:
        if not re.match(r'^\d{5}$', codigo_mpio):
            return Response(
                {'error': 'Código de municipio inválido (debe ser 5 dígitos)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        column_name = 'codigo_mpio'
        codigo = codigo_mpio
    else:
        if not re.match(r'^\d{2}$', codigo_dpto):
            return Response(
                {'error': 'Código de departamento inválido (debe ser 2 dígitos)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        column_name = 'codigo_dpto'
        codigo = codigo_dpto

    # Validate and sanitize filename
    nombre = request.GET.get('nombre', 'descarga_datos')[:50]
    nombre = re.sub(r'[^a-zA-Z0-9_-]', '', nombre) or 'descarga_datos'

    # Check if files already exists
    storage_dir = os.path.join(settings.MEDIA_ROOT, 'cached_zips')
    os.makedirs(storage_dir, exist_ok=True)
    file_path = os.path.join(storage_dir, f"reporte_{nombre}.zip")

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"reporte_{nombre}.zip")
    else:
        zip = generar_zip(codigo, column_name, nombre)

        # Adds code to json for future updates
        codigos_file = os.path.join(settings.MEDIA_ROOT, 'codes.json')

        if os.path.exists(codigos_file):
            with open(codigos_file, 'r') as f:
                codigos = json.load(f)

            dict = codigos.get('mpios', {}) if column_name == 'codigo_mpio' else codigos.get('dptos', {})

            if codigo not in dict:
                dict[codigo] = nombre
                with open(codigos_file, 'w') as fp:
                    json.dump(codigos, fp)

        response = HttpResponse(zip, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename=reporte_{nombre}.zip'
        return response
