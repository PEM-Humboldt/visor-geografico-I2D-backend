"""
Tests for Phase 3 advanced features: Data Validation, API Versioning, and Spatial Operations
"""
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from applications.common.validators import (
    department_validator, municipality_validator, 
    biodiversity_validator, gbif_validator, user_request_validator
)
from applications.common.middleware import (
    DataQualityMiddleware, ErrorHandlingMiddleware, 
    APIVersioningMiddleware, RequestLoggingMiddleware
)
from applications.common.spatial import (
    GeographicDataValidator, SpatialQueryOptimizer, 
    PostGISIntegrationAssessment
)


class DataValidationTestCase(TestCase):
    """Test comprehensive data validation"""
    
    def test_department_validation_comprehensive(self):
        """Test comprehensive department validation"""
        # Valid cases
        valid_departments = ['05', '11', '76', '25', '68']
        for dept in valid_departments:
            result = department_validator(dept)
            self.assertEqual(result, dept)
        
        # Invalid cases with specific error checking
        invalid_cases = [
            ('00', 'Invalid department code'),
            ('99', 'Invalid department code'),
            ('ABC', 'must contain only digits'),
            ('123', 'must be exactly 2 digits'),
            ('', 'must be exactly 2 digits'),
            (None, 'must be a string'),
            (123, 'must be a string')
        ]
        
        for invalid_input, expected_error in invalid_cases:
            with self.assertRaises(ValidationError) as context:
                department_validator(invalid_input)
            self.assertIn(expected_error.lower(), str(context.exception).lower())
    
    def test_municipality_validation_comprehensive(self):
        """Test comprehensive municipality validation"""
        # Valid cases
        valid_municipalities = ['05001', '11001', '76001', '25001']
        for mpio in valid_municipalities:
            result = municipality_validator(mpio)
            self.assertEqual(result, mpio)
        
        # Invalid cases
        invalid_cases = [
            ('00001', 'Invalid department'),
            ('05999', 'Valid format but may not exist'),
            ('ABCDE', 'must contain only digits'),
            ('123', 'must be exactly 5 digits'),
            ('', 'must be exactly 5 digits')
        ]
        
        for invalid_input, _ in invalid_cases:
            with self.assertRaises(ValidationError):
                municipality_validator(invalid_input)
    
    def test_biodiversity_data_validation(self):
        """Test biodiversity data validation"""
        # Valid data types
        valid_types = ['especies', 'registros', 'familias', 'amenazadas']
        for data_type in valid_types:
            result = biodiversity_validator.validate_data_type(data_type)
            self.assertEqual(result, data_type.lower())
        
        # Case insensitive
        result = biodiversity_validator.validate_data_type('ESPECIES')
        self.assertEqual(result, 'especies')
        
        # Invalid data types
        with self.assertRaises(ValidationError):
            biodiversity_validator.validate_data_type('invalid_type')
    
    def test_gbif_species_validation(self):
        """Test GBIF species name validation"""
        # Valid species names
        valid_species = [
            'Quercus humboldtii',
            'Espeletia grandiflora',
            'Panthera onca',
            'Ara macao'
        ]
        
        for species in valid_species:
            result = gbif_validator.validate_species_name(species)
            self.assertEqual(result, species)
        
        # Invalid species names
        invalid_species = [
            'quercus humboldtii',  # lowercase genus
            'Quercus',  # missing species
            'QUERCUS HUMBOLDTII',  # all uppercase
            'Quercus humboldtii extra',  # too many parts
            ''  # empty
        ]
        
        for species in invalid_species:
            with self.assertRaises(ValidationError):
                gbif_validator.validate_species_name(species)
    
    def test_coordinate_validation_detailed(self):
        """Test detailed coordinate validation"""
        # Valid Colombian coordinates
        valid_coords = [
            (4.7110, -74.0721),  # Bogotá
            (6.2442, -75.5812),  # Medellín
            (3.4516, -76.5320),  # Cali
            (-4.0, -70.0),  # Southern Colombia
            (15.0, -67.0)  # Northern Colombia
        ]
        
        for lat, lon in valid_coords:
            result_lat, result_lon = gbif_validator.validate_coordinates(lat, lon)
            self.assertEqual(result_lat, lat)
            self.assertEqual(result_lon, lon)
        
        # Invalid coordinates
        invalid_coords = [
            (20.0, -74.0),  # Too far north
            (-10.0, -74.0),  # Too far south
            (4.0, -60.0),  # Too far east
            (4.0, -90.0),  # Too far west
        ]
        
        for lat, lon in invalid_coords:
            with self.assertRaises(ValidationError):
                gbif_validator.validate_coordinates(lat, lon)


class MiddlewareTestCase(TestCase):
    """Test middleware functionality"""
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_data_quality_middleware(self):
        """Test data quality middleware"""
        middleware = DataQualityMiddleware(lambda r: None)
        
        # Test valid request
        request = self.factory.get('/api/test/')
        response = middleware.process_request(request)
        self.assertIsNone(response)  # Should pass through
        
        # Test request with suspicious content
        request = self.factory.get('/api/test/?param=DROP TABLE users')
        with patch('applications.common.middleware.logger') as mock_logger:
            response = middleware.process_request(request)
            mock_logger.warning.assert_called()
    
    def test_api_versioning_middleware(self):
        """Test API versioning middleware"""
        middleware = APIVersioningMiddleware(lambda r: None)
        
        # Test API request without version (should default to v1)
        request = self.factory.get('/api/test/')
        response = middleware.process_request(request)
        self.assertIsNone(response)
        self.assertEqual(request.api_version, 'v1')
        
        # Test API request with version header
        request = self.factory.get('/api/test/', HTTP_X_API_VERSION='v1')
        response = middleware.process_request(request)
        self.assertIsNone(response)
        self.assertEqual(request.api_version, 'v1')
        
        # Test unsupported version
        request = self.factory.get('/api/test/', HTTP_X_API_VERSION='v99')
        response = middleware.process_request(request)
        self.assertEqual(response.status_code, 400)
    
    def test_error_handling_middleware(self):
        """Test error handling middleware"""
        middleware = ErrorHandlingMiddleware(lambda r: None)
        
        # Test validation error handling
        request = self.factory.get('/api/test/')
        validation_error = ValidationError('Test validation error')
        
        response = middleware.process_exception(request, validation_error)
        self.assertEqual(response.status_code, 400)
        
        # Check response content
        import json
        content = json.loads(response.content)
        self.assertEqual(content['error'], 'Validation Error')
        self.assertIn('Test validation error', content['message'])


class SpatialOperationsTestCase(TestCase):
    """Test spatial operations and PostGIS integration"""
    
    def test_geographic_data_validator(self):
        """Test geographic data validation"""
        validator = GeographicDataValidator()
        
        # Test coordinate validation
        point = validator.validate_coordinates(4.7110, -74.0721)
        self.assertIsNotNone(point)
        
        # Test invalid coordinates
        with self.assertRaises(ValidationError):
            validator.validate_coordinates(50.0, -74.0)  # Outside Colombia
    
    def test_geometry_validation(self):
        """Test geometry data validation"""
        validator = GeographicDataValidator()
        
        # Test GeoJSON Point
        geojson_point = {
            'type': 'Point',
            'coordinates': [-74.0721, 4.7110]
        }
        
        geometry = validator.validate_geometry(geojson_point)
        self.assertIsNotNone(geometry)
        
        # Test invalid geometry
        with self.assertRaises(ValidationError):
            validator.validate_geometry({'invalid': 'data'})
    
    @patch('django.db.connection')
    def test_postgis_assessment(self, mock_connection):
        """Test PostGIS integration assessment"""
        # Mock PostGIS available
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ['PostGIS 3.4.0']
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        assessment = PostGISIntegrationAssessment.check_postgis_availability()
        self.assertTrue(assessment['available'])
        self.assertIn('PostGIS 3.4.0', assessment['version'])
        
        # Mock PostGIS not available
        mock_cursor.execute.side_effect = Exception('PostGIS not found')
        assessment = PostGISIntegrationAssessment.check_postgis_availability()
        self.assertFalse(assessment['available'])
    
    def test_spatial_query_optimizer(self):
        """Test spatial query optimization"""
        optimizer = SpatialQueryOptimizer()
        
        # Test optimization hints
        hints = optimizer.create_spatial_index_hints()
        self.assertIn('use_index', hints)
        self.assertIn('geometry_idx', hints['use_index'])


class APIVersioningTestCase(APITestCase):
    """Test API versioning functionality"""
    
    def test_version_header_support(self):
        """Test API version header support"""
        # Test with version header
        response = self.client.get('/api/docs/', HTTP_X_API_VERSION='v1')
        # Should not return version error
        self.assertNotEqual(response.status_code, 400)
    
    def test_accept_header_versioning(self):
        """Test Accept header versioning"""
        # Test with Accept header
        response = self.client.get(
            '/api/docs/', 
            HTTP_ACCEPT='application/vnd.humboldt.v1+json'
        )
        # Should not return version error
        self.assertNotEqual(response.status_code, 400)


class SecurityValidationTestCase(TestCase):
    """Test security-related validation"""
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "UNION SELECT * FROM users"
        ]
        
        for malicious_input in malicious_inputs:
            with self.assertRaises(ValidationError):
                user_request_validator.validate_institution(malicious_input)
    
    def test_xss_prevention(self):
        """Test XSS prevention"""
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>"
        ]
        
        for xss_input in xss_inputs:
            with self.assertRaises(ValidationError):
                user_request_validator.validate_observation(xss_input)
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        # Test whitespace trimming
        result = user_request_validator.validate_institution('  Test Institution  ')
        self.assertEqual(result, 'Test Institution')
        
        # Test length limits
        with self.assertRaises(ValidationError):
            user_request_validator.validate_institution('A' * 201)  # Too long


class DataIntegrityAdvancedTestCase(TestCase):
    """Advanced data integrity tests"""
    
    def test_cross_field_validation(self):
        """Test validation across multiple fields"""
        # Test municipality belongs to correct department
        valid_mpio = '05001'  # Medellín, Antioquia
        result = municipality_validator(valid_mpio)
        self.assertEqual(result, valid_mpio)
        
        # Extract department from municipality
        dept_code = valid_mpio[:2]
        dept_result = department_validator(dept_code)
        self.assertEqual(dept_result, dept_code)
    
    def test_data_consistency_checks(self):
        """Test data consistency validation"""
        # Test numeric value ranges
        valid_values = [0, 1, 100, 1000]
        for value in valid_values:
            result = biodiversity_validator.validate_numeric_value(value)
            self.assertGreaterEqual(result, 0)
        
        # Test with custom ranges
        result = biodiversity_validator.validate_numeric_value(50, min_value=10, max_value=100)
        self.assertEqual(result, 50)
        
        with self.assertRaises(ValidationError):
            biodiversity_validator.validate_numeric_value(5, min_value=10)
    
    def test_temporal_data_validation(self):
        """Test temporal data validation"""
        # Valid dates
        valid_dates = ['2023-01-15', '2020/12/31', '15-06-2021']
        for date_str in valid_dates:
            result = gbif_validator.validate_date_format(date_str)
            self.assertIsNotNone(result)
        
        # Future dates should be invalid
        with self.assertRaises(ValidationError):
            gbif_validator.validate_date_format('2030-01-01')
        
        # Very old dates should be invalid
        with self.assertRaises(ValidationError):
            gbif_validator.validate_date_format('1700-01-01')
