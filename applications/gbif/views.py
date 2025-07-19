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

from .models import gbifInfo
from .serializers import gbifInfoSerializer

class GbifInfo(ListAPIView):
    serializer_class=gbifInfoSerializer

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

@api_view(['GET'])
def descargarzip(request):
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
        where = "WHERE codigo_mpio = %s"
        params.append(filtro["codigo_mpio"])
    elif filtro.get("codigo_dpto"):
        where = "WHERE codigo_dpto = %s"
        params.append(filtro["codigo_dpto"])

    registros_query = f"SELECT * FROM gbif.gbif {where}"
    especies_query = f"""
        SELECT DISTINCT reino, filo, clase, orden, familia, genero, especies, endemicas, amenazadas, exoticas
        FROM gbif.lista_especies_consulta {where}
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