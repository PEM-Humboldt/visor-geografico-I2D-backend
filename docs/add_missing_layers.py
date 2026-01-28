#!/usr/bin/env python3
"""
Add missing layer groups to the general project using Django ORM
"""
import os
import sys
import django

# Setup Django environment
# Add the backend directory to Python path using relative path
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i2dbackend.settings.local')
django.setup()

from applications.projects.models import Project, LayerGroup, Layer
def main():
    try:
        # Get the general project
        project = Project.objects.get(nombre_corto='general')
        print(f'Adding layer groups to project: {project.nombre}')

        # Create the missing layer groups
        layer_groups_data = [
            {'nombre': 'Proyecto Oleoducto Bicentenario', 'orden': 7},
            {'nombre': 'Gobernanza', 'orden': 6},
            {'nombre': 'Restauración', 'orden': 4},
            {'nombre': 'Conflictos socioambientales en páramos', 'orden': 0}
        ]

        created_groups = {}
        for group_data in layer_groups_data:
            lg, created = LayerGroup.objects.get_or_create(
                nombre=group_data['nombre'],
                proyecto=project,
                defaults={
                    'orden': group_data['orden'],
                    'fold_state': 'close',
                    'parent_group': None
                }
            )
            created_groups[group_data['nombre']] = lg
            print(f'Layer group "{group_data["nombre"]}": {"Created" if created else "Already exists"}')

        print('\nAdding layers to groups...')

        # Add layer for Proyecto Oleoducto Bicentenario
        oleoducto_group = created_groups['Proyecto Oleoducto Bicentenario']
        Layer.objects.get_or_create(
            nombre_geoserver='coberturas_bo_2009_2010',
            grupo=oleoducto_group,
            defaults={
                'nombre_display': 'Cobertura Bo',
                'store_geoserver': 'Proyecto_oleoducto_bicentenario',
                'estado_inicial': False,
                'metadata_id': '008150a7-4ee9-488a-9ac0-354d678b4b8e',
                'orden': 1
            }
        )

        # Add layer for Gobernanza
        gobernanza_group = created_groups['Gobernanza']
        Layer.objects.get_or_create(
            nombre_geoserver='procesos_gobernanza',
            grupo=gobernanza_group,
            defaults={
                'nombre_display': 'Posibles procesos de gobernanza',
                'store_geoserver': 'Gobernanza',
                'estado_inicial': False,
                'metadata_id': 'a6fcfe1b-11e8-4383-a38e-a7f0035dece5',
                'orden': 1
            }
        )

        # Add layers for Restauración
        restauracion_group = created_groups['Restauración']
        restauracion_layers = [
            {'geoserver': 'integr_total4326', 'display': 'Integridad', 'store_geoserver': 'restauracion', 'metadata': '55d29ef5-e419-489f-a450-3299e4bcc4d4', 'orden': 1},
            {'geoserver': 'red_viveros', 'display': 'Red Viveros',  'store_geoserver': 'visor', 'metadata': None, 'orden': 2},
            {'geoserver': 'scen_mincost_target1', 'display': 'Escenario mínimo costo target 1', 'store_geoserver': 'weplan', 'metadata': '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 'orden': 3},
            {'geoserver': 'scen_mincost_target2', 'display': 'Escenario mínimo costo target 2', 'store_geoserver': 'weplan', 'metadata': '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 'orden': 4},
            {'geoserver': 'scen_mincost_target3', 'display': 'Escenario mínimo costo target 3', 'store_geoserver': 'weplan', 'metadata': '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 'orden': 5},
            {'geoserver': 'scen_mincost_target4', 'display': 'Escenario mínimo costo target 4', 'store_geoserver': 'weplan', 'metadata': '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 'orden': 6}
        ]

        for layer_data in restauracion_layers:
            Layer.objects.get_or_create(
                nombre_geoserver=layer_data['geoserver'],
                grupo=restauracion_group,
                defaults={
                    'nombre_display': layer_data['display'],
                    'store_geoserver': layer_data['store_geoserver'],
                    'estado_inicial': False,
                    'metadata_id': layer_data['metadata'],
                    'orden': layer_data['orden']
                }
            )

        # Add layers for Conflictos socioambientales en páramos
        gef_paramos_group = created_groups['Conflictos socioambientales en páramos']
        Layer.objects.get_or_create(
            nombre_geoserver='paramo',
            grupo=gef_paramos_group,
            defaults={
                'nombre_display': 'Paramos',
                'store_geoserver': 'gefparamos',
                'estado_inicial': False,
                'orden': 1
            }
        )
        Layer.objects.get_or_create(
            nombre_geoserver='municipio',
            grupo=gef_paramos_group,
            defaults={
                'nombre_display': 'Municipios',
                'store_geoserver': 'gefparamos',
                'estado_inicial': False,
                'orden': 2
            }
        )

        print('\nFinal layer group count for general project:')
        total_groups = LayerGroup.objects.filter(proyecto=project).count()
        print(f'Total layer groups: {total_groups}')

        for lg in LayerGroup.objects.filter(proyecto=project).order_by('orden'):
            layer_count = Layer.objects.filter(grupo=lg).count()
            print(f'  - {lg.nombre}: {layer_count} layers')

        print('\nSuccess! Missing layer groups and layers have been added to the general project.')

    except Exception as e:
        print(f'Error: {e}')
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
