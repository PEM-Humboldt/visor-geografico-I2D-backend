from django.core.management.base import BaseCommand
import os
import json
import traceback
from applications.gbif.utils import *
from django.utils import timezone
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        def now():
            return f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        
        codigos_file = os.path.join(settings.MEDIA_ROOT, 'codes.json')

        if os.path.exists(codigos_file):
            try:
                with open(codigos_file, 'r') as f:
                    codigos = json.load(f)
                    mpios_dict = codigos.get('mpios', {})
                    dptos_dict = codigos.get('dptos', {})
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR(f"{now()} - Error parsing JSON."))
                return
        else:
            self.stdout.write(self.style.ERROR(f"{now()} - File not found. Skipping."))
            return


        output_dir = os.path.join(settings.MEDIA_ROOT, 'cached_zips')
        os.makedirs(output_dir, exist_ok=True)

        stats = {"success": 0, "failed": 0}

        for codigo, nombre in mpios_dict.items():
            try:
                self.stdout.write(f"Generating ZIP at {now()} for {nombre} - {codigo}...")
                generar_zip(codigo, 'codigo_mpio', nombre)
                stats["success"] += 1
            except Exception as e:
                stats["failed"] += 1
                self.stdout.write(self.style.ERROR(f"FAILED at {now()} - ERROR generating ZIP for Municipio: {nombre} ({codigo}). Error: {str(e)}"))
                self.stdout.write(traceback.format_exc())

        for codigo, nombre in dptos_dict.items():
            try:
                self.stdout.write(f"Generating ZIP at {now()} for {nombre} - {codigo}...")
                generar_zip(codigo, 'codigo_dpto', nombre)
                stats["success"] += 1
            except Exception as e:
                stats["failed"] += 1
                self.stdout.write(self.style.ERROR(f"FAILED at {now()} - ERROR generating ZIP for Departamento: {nombre} ({codigo}). Error: {str(e)}"))
                self.stdout.write(traceback.format_exc())

        self.stdout.write(self.style.SUCCESS(f"ZIP generation completed at {now()}. Summary: {stats['success']} succeeded, {stats['failed']} failed."))
