from django.core.management.base import BaseCommand
import traceback
from applications.gbif.utils import generate_zip
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        def now():
            return f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        
        query = """
            SELECT 
                m.codigo AS mpio_codigo,
                m.nombre AS mpio_nombre,
                d.codigo AS dpto_codigo,
                d.nombre AS dpto_nombre
            FROM capas_base.mpio_politico m
            INNER JOIN capas_base.dpto_politico d ON LEFT(m.codigo, 2) = d.codigo
            ORDER BY dpto_codigo;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            # Fetchall returns a list of tuples, we convert them to dicts for ease of use
            columns = [col[0] for col in cursor.description]
            codes = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        stats = {"success": 0, "failed": 0}
        zipped_dptos = set()

        for code in codes:

            # Generate mpios zip
            try:
                mpio_code = code['mpio_codigo']
                mpio_name = code['mpio_nombre']

                self.stdout.write(f"Generating ZIP at {now()} for MPIO {mpio_name} - {mpio_code}...")
                generate_zip(mpio_code, 'codigo_mpio', mpio_name)
                stats["success"] += 1
            except Exception as e:
                stats["failed"] += 1
                self.stdout.write(self.style.ERROR(f"FAILED at {now()} - ERROR generating ZIP for Municipio: {mpio_name} - {mpio_code}. Error: {str(e)}"))
                self.stdout.write(traceback.format_exc())

            # Generate dptos zip only if it hasn't been generated already
            dpto_code = code['dpto_codigo']
            if dpto_code not in zipped_dptos:
                try:
                    dpto_name = code['dpto_nombre']

                    self.stdout.write(f"=== Generating ZIP at {now()} for DPTO {dpto_name} - {dpto_code}...")
                    generate_zip(dpto_code, 'codigo_dpto', dpto_name)
                    stats["success"] += 1
                    zipped_dptos.add(dpto_code)
                except Exception as e:
                    stats["failed"] += 1
                    self.stdout.write(self.style.ERROR(f"FAILED at {now()} - ERROR generating ZIP for Department: {dpto_name} - {dpto_code}. Error: {str(e)}"))
                    self.stdout.write(traceback.format_exc())

        self.stdout.write(self.style.SUCCESS(f"ZIP generation completed at {now()}. Summary: {stats['success']} succeeded, {stats['failed']} failed."))
