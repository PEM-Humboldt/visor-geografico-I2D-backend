import io
import os
import csv
import json
import zipfile
from django.db import connection
from django.conf import settings

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

def generar_zip(codigo, column_name, nombre):
    # Check directory
    output_dir = os.path.join(settings.MEDIA_ROOT, 'cached_zips')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"reporte_{nombre}.zip")

    # Use parameterized queries to prevent SQL injection
    registros_query = f"""
        SELECT * FROM gbif.gbif WHERE {column_name} = %s
    """

    especies_query = f"""
        SELECT DISTINCT reino, filo, clase, orden, familia, genero, especies, 
        endemicas, amenazadas, exoticas 
        FROM gbif.lista_especies_consulta WHERE {column_name} = %s
    """

    # Execute with parameters (prevents SQL injection)
    registros_csv = generar_csv(registros_query, [codigo])
    especies_csv = generar_csv(especies_query, [codigo])

    # Writes and saves newly generated zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('registros.csv', registros_csv)
        zip_file.writestr('lista_especies.csv', especies_csv)
        
    zip = zip_buffer.getvalue()
    with open(file_path, 'wb') as f:
        f.write(zip)

    return zip

