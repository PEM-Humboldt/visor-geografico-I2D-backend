"""
PostGIS integration and spatial operations for Visor I2D Backend
"""
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models import Q
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class SpatialQueryOptimizer:
    """Optimize spatial queries for better performance"""
    
    @staticmethod
    def optimize_point_in_polygon_query(point, polygon_queryset):
        """Optimize point-in-polygon queries"""
        try:
            # Use spatial index for initial filtering
            bbox = polygon_queryset.aggregate(
                extent=models.Extent('geometry')
            )['extent']
            
            if bbox:
                # Create bounding box filter first
                bbox_polygon = Polygon.from_bbox(bbox)
                filtered_queryset = polygon_queryset.filter(
                    geometry__bboverlaps=bbox_polygon
                )
                
                # Then apply precise point-in-polygon test
                return filtered_queryset.filter(geometry__contains=point)
            
            return polygon_queryset.filter(geometry__contains=point)
            
        except Exception as e:
            logger.error(f"Spatial query optimization error: {e}")
            return polygon_queryset.filter(geometry__contains=point)
    
    @staticmethod
    def optimize_distance_query(center_point, distance_km, queryset):
        """Optimize distance-based queries"""
        try:
            distance_obj = Distance(km=distance_km)
            
            # Use bounding box pre-filter for performance
            bbox_filter = Q(
                geometry__distance_lte=(center_point, distance_obj)
            )
            
            return queryset.filter(bbox_filter)
            
        except Exception as e:
            logger.error(f"Distance query optimization error: {e}")
            return queryset
    
    @staticmethod
    def create_spatial_index_hints():
        """Generate SQL hints for spatial index usage"""
        return {
            'use_index': ['geometry_idx', 'spatial_idx'],
            'force_index': 'geometry'
        }


class GeographicDataValidator:
    """Enhanced geographic data validation with PostGIS support"""
    
    COLOMBIA_BOUNDS = {
        'min_lat': -4.5,
        'max_lat': 16.0,
        'min_lon': -82.0,
        'max_lon': -66.0
    }
    
    def validate_coordinates(self, latitude, longitude):
        """Validate coordinates are within Colombian territory"""
        try:
            lat = float(latitude)
            lon = float(longitude)
        except (ValueError, TypeError):
            raise ValidationError('Coordinates must be valid numbers')
        
        if not (self.COLOMBIA_BOUNDS['min_lat'] <= lat <= self.COLOMBIA_BOUNDS['max_lat']):
            raise ValidationError(f'Latitude {lat} is outside Colombian territory')
        
        if not (self.COLOMBIA_BOUNDS['min_lon'] <= lon <= self.COLOMBIA_BOUNDS['max_lon']):
            raise ValidationError(f'Longitude {lon} is outside Colombian territory')
        
        return Point(lon, lat, srid=4326)
    
    def validate_geometry(self, geometry_data):
        """Validate geometry data structure"""
        if not geometry_data:
            raise ValidationError('Geometry data is required')
        
        try:
            if isinstance(geometry_data, dict):
                # GeoJSON format
                geom_type = geometry_data.get('type')
                coordinates = geometry_data.get('coordinates')
                
                if geom_type == 'Point':
                    return Point(coordinates, srid=4326)
                elif geom_type == 'Polygon':
                    return Polygon(coordinates[0], srid=4326)
                elif geom_type == 'MultiPolygon':
                    polygons = [Polygon(poly[0]) for poly in coordinates]
                    return MultiPolygon(polygons, srid=4326)
            
            # WKT format
            elif isinstance(geometry_data, str):
                from django.contrib.gis.geos import GEOSGeometry
                return GEOSGeometry(geometry_data, srid=4326)
            
            raise ValidationError('Unsupported geometry format')
            
        except Exception as e:
            raise ValidationError(f'Invalid geometry data: {str(e)}')
    
    def validate_spatial_relationship(self, geom1, geom2, relationship='intersects'):
        """Validate spatial relationships between geometries"""
        valid_relationships = [
            'intersects', 'contains', 'within', 'touches', 
            'crosses', 'overlaps', 'disjoint'
        ]
        
        if relationship not in valid_relationships:
            raise ValidationError(f'Invalid spatial relationship: {relationship}')
        
        try:
            method = getattr(geom1, relationship)
            return method(geom2)
        except Exception as e:
            raise ValidationError(f'Spatial relationship validation error: {str(e)}')


class SpatialAPIEndpoints:
    """Enhanced spatial API endpoints"""
    
    def __init__(self):
        self.validator = GeographicDataValidator()
        self.optimizer = SpatialQueryOptimizer()
    
    def find_species_by_location(self, latitude, longitude, radius_km=10):
        """Find species within radius of coordinates"""
        try:
            point = self.validator.validate_coordinates(latitude, longitude)
            
            # This would integrate with actual GBIF model when PostGIS is enabled
            # For now, return structure for future implementation
            return {
                'center_point': {'lat': latitude, 'lon': longitude},
                'radius_km': radius_km,
                'species_count': 0,
                'species': [],
                'message': 'PostGIS integration required for spatial queries'
            }
            
        except ValidationError as e:
            return {'error': str(e)}
    
    def get_administrative_boundaries(self, geometry):
        """Get administrative boundaries containing geometry"""
        try:
            validated_geom = self.validator.validate_geometry(geometry)
            
            # Future implementation with PostGIS
            return {
                'departments': [],
                'municipalities': [],
                'message': 'PostGIS integration required for boundary queries'
            }
            
        except ValidationError as e:
            return {'error': str(e)}
    
    def calculate_biodiversity_density(self, polygon_geometry):
        """Calculate biodiversity density within polygon"""
        try:
            polygon = self.validator.validate_geometry(polygon_geometry)
            area_km2 = polygon.transform(3857, clone=True).area / 1000000  # Convert to km²
            
            # Future implementation with actual data
            return {
                'area_km2': round(area_km2, 2),
                'species_density': 0,
                'total_species': 0,
                'message': 'PostGIS integration required for density calculations'
            }
            
        except ValidationError as e:
            return {'error': str(e)}


# PostGIS Integration Assessment
class PostGISIntegrationAssessment:
    """Assess current PostGIS integration status and recommendations"""
    
    @staticmethod
    def check_postgis_availability():
        """Check if PostGIS is available in current database"""
        from django.db import connection
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT PostGIS_Version();")
                version = cursor.fetchone()
                return {
                    'available': True,
                    'version': version[0] if version else 'Unknown',
                    'status': 'PostGIS is available'
                }
        except Exception as e:
            return {
                'available': False,
                'version': None,
                'status': f'PostGIS not available: {str(e)}'
            }
    
    @staticmethod
    def assess_current_geometry_fields():
        """Assess current geometry field usage"""
        from django.apps import apps
        
        geometry_fields = []
        text_geometry_fields = []
        
        for model in apps.get_models():
            for field in model._meta.get_fields():
                field_name = f"{model._meta.app_label}.{model._meta.model_name}.{field.name}"
                
                # Check for actual GeometryField
                if hasattr(field, 'geom_type'):
                    geometry_fields.append({
                        'model': field_name,
                        'type': field.geom_type,
                        'srid': getattr(field, 'srid', 'Unknown')
                    })
                
                # Check for text fields that might contain geometry
                elif hasattr(field, 'max_length') and field.name.lower() in ['geometry', 'geom', 'shape']:
                    text_geometry_fields.append(field_name)
        
        return {
            'geometry_fields': geometry_fields,
            'text_geometry_fields': text_geometry_fields,
            'total_geometry_fields': len(geometry_fields),
            'potential_conversions': len(text_geometry_fields)
        }
    
    @staticmethod
    def generate_migration_recommendations():
        """Generate recommendations for PostGIS migration"""
        postgis_status = PostGISIntegrationAssessment.check_postgis_availability()
        field_assessment = PostGISIntegrationAssessment.assess_current_geometry_fields()
        
        recommendations = {
            'postgis_status': postgis_status,
            'current_fields': field_assessment,
            'recommendations': []
        }
        
        if not postgis_status['available']:
            recommendations['recommendations'].extend([
                'Install PostGIS extension in PostgreSQL database',
                'Update Django settings to use django.contrib.gis.db.backends.postgis',
                'Add django.contrib.gis to INSTALLED_APPS'
            ])
        
        if field_assessment['text_geometry_fields']:
            recommendations['recommendations'].extend([
                'Convert text geometry fields to proper GeometryField',
                'Create data migration to parse existing geometry data',
                'Add spatial indexes for performance optimization'
            ])
        
        recommendations['recommendations'].extend([
            'Implement spatial query optimization',
            'Add geographic data validation',
            'Create spatial API endpoints',
            'Add spatial data integrity tests'
        ])
        
        return recommendations


# Initialize spatial components
spatial_validator = GeographicDataValidator()
spatial_optimizer = SpatialQueryOptimizer()
spatial_api = SpatialAPIEndpoints()
