from django.core.management.base import BaseCommand
from applications.projects.models import Project, LayerGroup, Layer, DefaultLayer


class Command(BaseCommand):
    help = 'Populate database with existing project configurations'

    def handle(self, *args, **options):
        self.stdout.write('Starting project data population...')
        
        # Create General Project
        general_project, created = Project.objects.get_or_create(
            nombre_corto='general',
            defaults={
                'nombre': 'Visor General I2D',
                'nivel_zoom': 6.0,
                'coordenada_central_x': -8113332,
                'coordenada_central_y': 464737,
                'panel_visible': True,
                'base_map_visible': 'streetmap'
            }
        )
        if created:
            self.stdout.write(f'Created project: {general_project.nombre}')
        
        # Create Ecoreservas Project
        ecoreservas_project, created = Project.objects.get_or_create(
            nombre_corto='ecoreservas',
            defaults={
                'nombre': 'Ecoreservas',
                'nivel_zoom': 9.2,
                'coordenada_central_x': -8249332,
                'coordenada_central_y': 544737,
                'panel_visible': True,
                'base_map_visible': 'cartodb_positron'
            }
        )
        if created:
            self.stdout.write(f'Created project: {ecoreservas_project.nombre}')

        # Create layer groups for General project
        if general_project:
            self.create_general_project_layers(general_project)
        
        # Create layer groups for Ecoreservas project
        if ecoreservas_project:
            self.create_ecoreservas_project_layers(ecoreservas_project)
            
        self.stdout.write(self.style.SUCCESS('Successfully populated project data'))

    def create_general_project_layers(self, project):
        """Create layer groups and layers for general project"""
        
        # Historicos group
        historicos_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Historicos',
            defaults={'orden': 1, 'fold_state': 'close'}
        )
        
        # Add layers to Historicos
        historicos_layers = [
            ('aicas', 'AICAS', 'Historicos', False, '09ee583d-d397-4eb8-99df-92bb6f0d0c4c'),
            ('bosque_seco_tropical', 'Bosque Seco Tropical 2014', 'Historicos', False, 'eca845f9-dea1-4e86-b562-27338b79ef29'),
            ('BST2018', 'Bosque Seco Tropical 2018', 'Historicos', False, '6ccd867c-5114-489f-9266-3e5cf657a375'),
            ('complejos_paramos_escala100k', 'Complejos Páramos Escala 100k', 'Historicos', False, 'c9a5d546-33b5-41d6-a60e-57cfae1cff82'),
            ('ecosistemas_cuenca_rio_orinoco', 'Ecosistemas Cuenca Río Orinoco', 'Historicos', False, '05281f18-d63e-469d-a2df-5796e8fd1769'),
            ('ecosistemas_generales_etter', 'Ecosistemas Generales Etter', 'Historicos', False, '52be9cc9-a139-4568-8781-bbbda5590eab'),
            ('grado_transformacion_humedales_m10k', 'Grado Transformación Humedales', 'Historicos', False, '532e5414-8906-47ee-a298-a97735fc6cdd'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(historicos_layers):
            Layer.objects.get_or_create(
                grupo=historicos_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )

        # Fondo de adaptación group
        fondo_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Fondo de adaptación',
            defaults={'orden': 2, 'fold_state': 'close'}
        )
        
        fondo_layers = [
            ('Humedales', 'Clasificación de humedales 2015', 'Proyecto_fondo_adaptacion', False, '7ff0663a-129c-43e9-a024-7718dbe59d60'),
            ('Humedales_Continentales_Insulares_2015_Vector', 'Humedales Continentales Insulares', 'Proyecto_fondo_adaptacion', False, 'd68f4329-0385-47a2-8319-8b56c772b4c0'),
            ('Limites21Paramos_25K_2015', 'Límite 21 Complejos Páramo 2015', 'Proyecto_fondo_adaptacion', False, '5dbddd78-3e51-45e6-b754-ab4c8f74f1b5'),
            ('Limites24Paramos_25K_2016', 'Límite 24 Complejos Páramo 2016', 'Proyecto_fondo_adaptacion', False, '36139b13-b15e-445e-b44d-dd7a5dbe8185'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(fondo_layers):
            Layer.objects.get_or_create(
                grupo=fondo_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )

        # Conservación de la Biodiversidad group
        conservacion_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Conservación de la Biodiversidad',
            defaults={'orden': 3, 'fold_state': 'close'}
        )
        
        conservacion_layers = [
            ('biomas', 'Biomas', 'Proyecto_PACBAO_Ecopetrol', False, '4ea0ecd2-678d-423b-a940-ee2667d6d4a2'),
            ('colapso_acuatico', 'Colapso Acuático', 'Proyecto_PACBAO_Ecopetrol', False, '11d7eb22-f60e-446f-b953-cb88817a4ca5'),
            ('colapso_terrestre', 'Colapso Terrestre', 'Proyecto_PACBAO_Ecopetrol', False, '11d7eb22-f60e-446f-b953-cb88817a4ca5'),
            ('colapso_total', 'Colapso Total', 'Proyecto_PACBAO_Ecopetrol', False, '11d7eb22-f60e-446f-b953-cb88817a4ca5'),
            ('distritos_biogeograficos', 'Distritos Biogeográficos', 'Proyecto_PACBAO_Ecopetrol', False, '2dec7ad8-6677-4ee2-912c-bd39af420952'),
            ('hidrobiologia', 'Hidrobiología', 'Proyecto_PACBAO_Ecopetrol', False, 'ca8b1ba9-3dea-4791-bf01-48df68d0fd41'),
            ('lineamientos', 'Lineamientos', 'Proyecto_PACBAO_Ecopetrol', False, '7963d97d-ba67-4c09-8f28-2807f43f9419'),
            ('meta_conservacion', 'Meta Conservación', 'Proyecto_PACBAO_Ecopetrol', False, '4cd64685-b856-42b7-a6ce-c4446abb36d3'),
            ('unicidad', 'Unicidad', 'Proyecto_PACBAO_Ecopetrol', False, '9c0dc2c7-6919-400d-998e-265624c7e781'),
            ('unidades_analisis', 'Unidades de Análisis', 'Proyecto_PACBAO_Ecopetrol', False, 'f6f304bd-a5f0-450c-a836-d30b12acbaff'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(conservacion_layers):
            Layer.objects.get_or_create(
                grupo=conservacion_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )

    def create_ecoreservas_project_layers(self, project):
        """Create layer groups and layers for ecoreservas project"""
        
        # Preservación - Compensación group
        comp_preservacion_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Preservación',
            defaults={'orden': 1, 'fold_state': 'close'}
        )
        
        preservacion_comp_layers = [
            ('Preservación_priorizando_todos_los_enfoques_Compensación', 'Todos los enfoques de costos-Inversión en compensación', 'ecoreservas', True, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Preservación_priorizando_Costos_de_Oportunidad_Compensación', 'Costos de oportunidad-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Preservación_priorizando_Costos_Abióticos_Compensación', 'Costos ecológicos-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(preservacion_comp_layers):
            Layer.objects.get_or_create(
                grupo=comp_preservacion_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )

        # Restauración - Compensación group
        comp_restauracion_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Restauración',
            defaults={'orden': 2, 'fold_state': 'close'}
        )
        
        restauracion_comp_layers = [
            ('Restauración_priorizando_todos_los_enfoques_Compensación', 'Todos los enfoques de costos-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Restauración_priorizando_Costos_de_Oportunidad_Compensación', 'Costos de oportunidad-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Restauración_priorizando_Costos_Abióticos_Compensación', 'Costos ecológicos-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(restauracion_comp_layers):
            Layer.objects.get_or_create(
                grupo=comp_restauracion_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )

        # Uso Sostenible - Compensación group
        comp_uso_group, _ = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre='Uso Sostenible',
            defaults={'orden': 3, 'fold_state': 'close'}
        )
        
        uso_comp_layers = [
            ('Uso_Sostenible_priorizando_todos_los_enfoques_Compensación', 'Todos los enfoques de costos-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Uso_Sostenible_priorizando_Costos_de_Oportunidad_Compensación', 'Costos de oportunidad-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
            ('Uso_Sostenible_priorizando_Costos_Abióticos_Compensación', 'Costos ecológicos-Inversión en compensación', 'ecoreservas', False, '4eca511b-d4db-49bc-8efa-a1f20e7c45ac'),
        ]
        
        for i, (geoserver_name, display_name, store, initial_state, metadata_id) in enumerate(uso_comp_layers):
            Layer.objects.get_or_create(
                grupo=comp_uso_group,
                nombre_geoserver=geoserver_name,
                defaults={
                    'nombre_display': display_name,
                    'store_geoserver': store,
                    'estado_inicial': initial_state,
                    'metadata_id': metadata_id,
                    'orden': i
                }
            )
