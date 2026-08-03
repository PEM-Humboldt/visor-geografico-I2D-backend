import io
import os
import csv
import zipfile
import re
import boto3
import unicodedata
from django.db import connection
from django.conf import settings 

def connect_s3():
    return boto3.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT_URL,
        region_name=settings.S3_DEFAULT_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY
    )

def sanitize_name(name):
    nfd_name = unicodedata.normalize("NFD", name)
    no_accent_name = nfd_name.encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r'[^a-zA-Z0-9_-]', '', no_accent_name) or 'descarga_datos'

def generate_csv(query, params):
    output = io.StringIO()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        writer = csv.writer(output)
        writer.writerow(columns)
        for row in cursor:
            writer.writerow(row)
    return output.getvalue()

def generate_zip(codigo, column_name, name):

    clean_name = sanitize_name(name)

    s3_client = connect_s3()

    # Use parameterized queries to prevent SQL injection
    records_query = f"""
        SELECT * FROM gbif.gbif WHERE {column_name} = %s
    """

    species_query = f"""
        SELECT DISTINCT reino, filo, clase, orden, familia, genero, especies, 
        endemicas, amenazadas, exoticas 
        FROM gbif.lista_especies_consulta WHERE {column_name} = %s
    """

    # Execute with parameters (prevents SQL injection)
    records_csv = generate_csv(records_query, [codigo])
    species_csv = generate_csv(species_query, [codigo])

    # Writes and saves newly generated zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('registros.csv', records_csv)
        zip_file.writestr('lista_especies.csv', species_csv)
        
    zip = zip_buffer.getvalue()
    
    # Uploads file to bucket
    s3_client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=f'reporte_{clean_name}.zip',
        Body=zip,
    )

    zip_buffer.close()