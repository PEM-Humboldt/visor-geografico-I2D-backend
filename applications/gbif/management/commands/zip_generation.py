from django.core.management.base import BaseCommand
import os
import json
from applications.gbif.utils import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        codigos_file = os.path.join(os.getenv('MEDIA_ROOT', '/app/media'), 'codes.json')

        if os.path.exists(codigos_file):
            with open(codigos_file, 'r') as f:
                codigos = json.load(f)
                mpios_dict = codigos.get('mpios', {})
                dptos_dict = codigos.get('dptos', {})

        output_dir = os.path.join(os.getenv('MEDIA_ROOT', '/app/media'), 'cached_zips')
        os.makedirs(output_dir, exist_ok=True)

        for codigo, nombre in mpios_dict.items():
            self.stdout.write(f"Generating ZIP for {nombre} - {codigo}...")

            generar_zip(codigo, 'codigo_mpio', nombre)

        for codigo, nombre in dptos_dict.items():
            self.stdout.write(f"Generating ZIP for {nombre} - {codigo}...")

            generar_zip(codigo, 'codigo_dpto', nombre)
                
        self.stdout.write(self.style.SUCCESS("ZIP generation complete"))
