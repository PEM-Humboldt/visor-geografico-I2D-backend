from django.shortcuts import render
import io
import csv
import zipfile
from django.http import HttpResponse
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

def generar_csv(query, params):
    output = io.StringIO()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        writer = csv.writer(output)
        writer.writerow(columns)
        for row in cursor:
            writer.writerow(row)
    return output.getvalue()

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
    """
    filtro = {}
    if request.GET.get('codigo_mpio'):
        filtro["codigo_mpio"] = request.GET['codigo_mpio']
    elif request.GET.get('codigo_dpto'):
        filtro["codigo_dpto"] = request.GET['codigo_dpto']
    else:
        return Response({'error': 'Debe proporcionar codigo_mpio o codigo_dpto'}, status=status.HTTP_400_BAD_REQUEST)

    nombre = request.GET.get('nombre', 'descarga_datos')
    # Limpiar el nombre para evitar caracteres no válidos
    nombre = "".join(c for c in nombre if c.isalnum() or c in (' ', '_', '-')).rstrip()

    # Generar CSVs
    where = ""
    params = []
    if filtro.get("codigo_mpio"):
        where = "WHERE codigo = %s"
        params.append(filtro["codigo_mpio"])
    elif filtro.get("codigo_dpto"):
        where = "WHERE codigo = %s"
        params.append(filtro["codigo_dpto"])

    # Use existing tables from gbif_consultas schema
    registros_query = f"SELECT codigo, tipo, registers, species, exoticas, endemicas, nombre FROM gbif_consultas.mpio_queries {where}" if filtro.get("codigo_mpio") else f"SELECT codigo, tipo, registers, species, exoticas, endemicas, nombre FROM gbif_consultas.dpto_queries {where}"
    especies_query = f"""
        SELECT DISTINCT 'Animalia' as reino, '' as filo, '' as clase, '' as orden, '' as familia, '' as genero,
               species as especies, endemicas, 0 as amenazadas, exoticas
        FROM gbif_consultas.mpio_queries {where}
    """ if filtro.get("codigo_mpio") else f"""
        SELECT DISTINCT 'Animalia' as reino, '' as filo, '' as clase, '' as orden, '' as familia, '' as genero,
               species as especies, endemicas, 0 as amenazadas, exoticas
        FROM gbif_consultas.dpto_queries {where}
    """

    registros_csv = generar_csv(registros_query, params)
    especies_csv = generar_csv(especies_query, params)

    # Empaquetar ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('registros.csv', registros_csv)
        zip_file.writestr('lista_especies.csv', especies_csv)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={nombre}.zip'
    return response
