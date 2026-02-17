#!/usr/bin/env python3
"""
Script to create missing groups and layers for the ecoreservas project
based on the production HTML structure.
"""

import os
import sys
import django
import json

# Add the Django project to the Python path
sys.path.append('/home/mrueda/WWW/humboldt/visor-geografico-I2D-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i2dbackend.settings')
django.setup()

from applications.projects.models import Project, LayerGroup, Layer

def create_ecoreservas_structure():
    """Create the complete ecoreservas project structure"""
    
    # Get or create the ecoreservas project
    project, created = Project.objects.get_or_create(
        nombre_corto='ecoreservas',
        defaults={
            'nombre': 'Ecoreservas',
            'nivel_zoom': 6.0,
            'coordenada_central_x': -74.0,
            'coordenada_central_y': 4.6,
            'panel_visible': True,
            'base_map_visible': 'streetmap'
        }
    )
    
    if created:
        print(f"Created project: {project}")
    else:
        print(f"Using existing project: {project}")
    
    # Structure based on the HTML provided
    structure = {
        "Ecoregión relacionada a las Ecoreservas Mancilla y Tocancipá": {
            "orden": 2,
            "color": "#17a2b8",
            "subgroups": {
                "Compensación": {
                    "orden": 0,
                    "color": "#28a745",
                    "subgroups": {
                        "Preservación": {
                            "orden": 0,
                            "layers": [
                                {
                                    "nombre_geoserver": "Preservación_priorizando_todos_los_enfoques_Compensación",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Restauración": {
                            "orden": 1,
                            "layers": [
                                {
                                    "nombre_geoserver": "Restauración_priorizando_todos_los_enfoques_Compensación",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Uso Sostenible": {
                            "orden": 2,
                            "layers": [
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_todos_los_enfoques_Compensación",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        }
                    }
                },
                "Inversión 1%": {
                    "orden": 1,
                    "color": "#28a745",
                    "subgroups": {
                        "Preservación": {
                            "orden": 0,
                            "layers": [
                                {
                                    "nombre_geoserver": "Preservación_priorizando_todos_los_enfoques_Compensación.",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación.",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Restauración": {
                            "orden": 1,
                            "layers": [
                                {
                                    "nombre_geoserver": "Restauración_priorizando_todos_los_enfoques_Compensación",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Uso Sostenible": {
                            "orden": 2,
                            "layers": [
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_todos_los_enfoques_Compensación",
                                    "nombre_display": "Todos los enfoques de costos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_de_Oportunidad_Compensación",
                                    "nombre_display": "Costos de oportunidad-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_Abióticos_Compensación",
                                    "nombre_display": "Costos ecológicos-Inversión en compensación",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        }
                    }
                },
                "Inversión Voluntaria": {
                    "orden": 2,
                    "color": "#28a745",
                    "subgroups": {
                        "Preservación": {
                            "orden": 0,
                            "layers": [
                                {
                                    "nombre_geoserver": "Preservación_priorizando_todos_los_enfoques_Inversión_Voluntaria",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Preservación_riorizando_Costos_de_Oportunidad_Inversión_Voluntaria",
                                    "nombre_display": "Costos de oportunidad-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_Abióticos_Inversión_Voluntaria",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Restauración": {
                            "orden": 1,
                            "layers": [
                                {
                                    "nombre_geoserver": "Restauración_priorizando_todos_los_enfoques_Inversión_Voluntaria",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Restauración_Costos_de_Oportunidad_Inversión_Voluntaria",
                                    "nombre_display": "Costos de oportunidad-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_Abióticos_Inversión_Voluntaria",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        },
                        "Uso Sostenible": {
                            "orden": 2,
                            "layers": [
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_todos_los_enfoques_Inversión_Voluntaria",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_Costos_de_Oportunidad_Inversión_Voluntaria",
                                    "nombre_display": "Costos de oportunidad-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_Abióticos_Inversión_Voluntaria",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "4eca511b-d4db-49bc-8efa-a1f20e7c45ac",
                                    "orden": 2
                                }
                            ]
                        }
                    }
                }
            }
        },
        "Ecoregión relacionada a la Ecoreserva San Antero": {
            "orden": 3,
            "color": "#ffc107",
            "subgroups": {
                "Inversión 1%": {
                    "orden": 0,
                    "color": "#28a745",
                    "subgroups": {
                        "Preservación": {
                            "orden": 0,
                            "layers": [
                                {
                                    "nombre_geoserver": "Preservación_priorizando_todos_los_enfoques_Inversión_no_menos_1_",
                                    "nombre_display": "Todos los enfoques de costos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_de_Oportunidad_Inversión_no_menos_1_",
                                    "nombre_display": "Costos de oportunidad-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_Abióticos_Inversión_no_menos_1_",
                                    "nombre_display": "Costos ecológicos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        },
                        "Restauración": {
                            "orden": 1,
                            "layers": [
                                {
                                    "nombre_geoserver": "Restauración_priorizando_todos_los_enfoques_Inversión_no_menos_1_",
                                    "nombre_display": "Todos los enfoques de costos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Restauración_Costos_de_Oportunidad_Inversión_no_menos_1_",
                                    "nombre_display": "Costos de oportunidad-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_Abióticos_Inversión_no_menos_1_",
                                    "nombre_display": "Costos ecológicos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        },
                        "Uso Sostenible": {
                            "orden": 2,
                            "layers": [
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_todos_los_enfoques_Inversión_no_menos_1_",
                                    "nombre_display": "Todos los enfoques de costos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_de_Oportunidad_Inversión_no_menos_1_",
                                    "nombre_display": "Costos de oportunidad-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_Abióticos_Inversión_no_menos_1_",
                                    "nombre_display": "Costos ecológicos-Inversión no menos 1_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        }
                    }
                },
                "Inversión Voluntaria": {
                    "orden": 1,
                    "color": "#28a745",
                    "subgroups": {
                        "Preservación": {
                            "orden": 0,
                            "layers": [
                                {
                                    "nombre_geoserver": "Preservación_priorizando_todos_los_enfoques_Inversión_Voluntaria_",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Preservación_riorizando_Costos_de_Oportunidad_Inversión_Voluntaria_",
                                    "nombre_display": "Costos de oportunidad-Inversión Voluntaria_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Preservación_priorizando_Costos_Abióticos_Inversión_Voluntaria_",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        },
                        "Restauración": {
                            "orden": 1,
                            "layers": [
                                {
                                    "nombre_geoserver": "Restauración_priorizando_todos_los_enfoques_Inversión_Voluntaria_",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Restauración_Costos_de_Oportunidad_Inversión_Voluntaria_",
                                    "nombre_display": "Costos de oportunidad-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Restauración_priorizando_Costos_Abióticos_Inversión_Voluntaria_",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        },
                        "Uso Sostenible": {
                            "orden": 2,
                            "layers": [
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_todos_los_enfoques_Inversión_Voluntaria_",
                                    "nombre_display": "Todos los enfoques de costos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 0
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_Costos_de_Oportunidad_Inversión_Voluntaria_",
                                    "nombre_display": "Costos de oportunidad-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 1
                                },
                                {
                                    "nombre_geoserver": "Uso_Sostenible_priorizando_Costos_Abióticos_Inversión_Voluntaria_",
                                    "nombre_display": "Costos ecológicos-Inversiones voluntarias_",
                                    "store_geoserver": "ecoreservas",
                                    "estado_inicial": False,
                                    "metadata_id": "ddbae3f2-0a76-414f-bf76-8c0d681cd6c1",
                                    "orden": 2
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
    
    def create_group_recursive(name, config, parent_group=None):
        """Recursively create groups and subgroups"""
        group, created = LayerGroup.objects.get_or_create(
            proyecto=project,
            nombre=name,
            parent_group=parent_group,
            defaults={
                'orden': config.get('orden', 0),
                'color': config.get('color', '#e3e3e3'),
                'fold_state': 'close'
            }
        )
        
        if created:
            print(f"Created group: {name}")
        else:
            print(f"Using existing group: {name}")
        
        # Create layers if they exist
        if 'layers' in config:
            for layer_config in config['layers']:
                layer, layer_created = Layer.objects.get_or_create(
                    grupo=group,
                    nombre_geoserver=layer_config['nombre_geoserver'],
                    defaults={
                        'nombre_display': layer_config['nombre_display'],
                        'store_geoserver': layer_config['store_geoserver'],
                        'estado_inicial': layer_config['estado_inicial'],
                        'metadata_id': layer_config.get('metadata_id'),
                        'orden': layer_config['orden']
                    }
                )
                
                if layer_created:
                    print(f"  Created layer: {layer_config['nombre_display']}")
                else:
                    print(f"  Using existing layer: {layer_config['nombre_display']}")
        
        # Create subgroups recursively
        if 'subgroups' in config:
            for subgroup_name, subgroup_config in config['subgroups'].items():
                create_group_recursive(subgroup_name, subgroup_config, group)
        
        return group
    
    # Create the structure
    for group_name, group_config in structure.items():
        create_group_recursive(group_name, group_config)
    
    print("\n✅ Ecoreservas structure created successfully!")
    print(f"Total groups: {LayerGroup.objects.filter(proyecto=project).count()}")
    print(f"Total layers: {Layer.objects.filter(grupo__proyecto=project).count()}")

if __name__ == "__main__":
    create_ecoreservas_structure()