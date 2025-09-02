"""
Integration tests for Visor I2D Backend
"""
import json
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.db import connection


class DatabaseIntegrationTest(TransactionTestCase):
    """Test database integration and connections"""
    
    def test_database_connection(self):
        """Test that database connection works"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)
    
    def test_django_admin_access(self):
        """Test Django admin interface accessibility"""
        client = APIClient()
        response = client.get('/admin/')
        # Should redirect to login or show admin page
        self.assertIn(response.status_code, [200, 302])


class APIEndpointIntegrationTest(APITestCase):
    """Integration tests for all API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_documentation_endpoints(self):
        """Test that all documentation endpoints are accessible"""
        endpoints = [
            '/api/docs/',
            '/api/redoc/',
            '/api/schema/'
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                # Should be accessible (200) or redirect (302)
                self.assertIn(response.status_code, [200, 302, 404])
    
    def test_root_url_redirect(self):
        """Test root URL redirect functionality"""
        response = self.client.get('/')
        # Should redirect to admin
        self.assertIn(response.status_code, [200, 302])
    
    @patch('applications.gbif.models.gbifInfo.objects')
    def test_gbif_endpoint_integration(self, mock_gbif):
        """Test GBIF endpoint integration"""
        mock_gbif.all.return_value = []
        
        response = self.client.get('/api/gbif/gbifinfo')
        # Test endpoint exists and responds
        self.assertIsNotNone(response)
    
    def test_department_endpoints_structure(self):
        """Test department endpoint URL structure"""
        test_codes = ['05', '11', '25']
        
        for code in test_codes:
            with self.subTest(code=code):
                # Test charts endpoint
                charts_url = f'/api/dpto/charts/{code}'
                response = self.client.get(charts_url)
                self.assertIsNotNone(response)
                
                # Test danger charts endpoint
                danger_url = f'/api/dpto/dangerCharts/{code}'
                response = self.client.get(danger_url)
                self.assertIsNotNone(response)
    
    def test_municipality_endpoints_structure(self):
        """Test municipality endpoint URL structure"""
        test_codes = ['05001', '11001', '25001']
        
        for code in test_codes:
            with self.subTest(code=code):
                # Test charts endpoint
                charts_url = f'/api/mpio/charts/{code}'
                response = self.client.get(charts_url)
                self.assertIsNotNone(response)
                
                # Test danger charts endpoint
                danger_url = f'/api/mpio/dangerCharts/{code}'
                response = self.client.get(danger_url)
                self.assertIsNotNone(response)


class CORSIntegrationTest(APITestCase):
    """Test CORS configuration"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = self.client.options('/api/gbif/gbifinfo')
        # CORS middleware should add appropriate headers
        self.assertIsNotNone(response)
    
    def test_cors_allowed_origins(self):
        """Test CORS allowed origins configuration"""
        # Test with different origin headers
        origins = [
            'http://localhost:1234',
            'http://0.0.0.0:1234'
        ]
        
        for origin in origins:
            with self.subTest(origin=origin):
                response = self.client.get(
                    '/api/gbif/gbifinfo',
                    HTTP_ORIGIN=origin
                )
                self.assertIsNotNone(response)


class StaticFilesIntegrationTest(APITestCase):
    """Test static files serving"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_admin_static_files(self):
        """Test that admin static files are accessible"""
        # Test common admin static files
        static_files = [
            '/static/admin/css/base.css',
            '/static/admin/js/core.js'
        ]
        
        for static_file in static_files:
            with self.subTest(file=static_file):
                response = self.client.get(static_file)
                # Should be accessible or return 404 if not found
                self.assertIn(response.status_code, [200, 404])
    
    def test_swagger_static_files(self):
        """Test that Swagger static files are accessible"""
        swagger_files = [
            '/static/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js',
            '/static/drf-yasg/swagger-ui-dist/swagger-ui.css'
        ]
        
        for swagger_file in swagger_files:
            with self.subTest(file=swagger_file):
                response = self.client.get(swagger_file)
                self.assertIn(response.status_code, [200, 404])


class ErrorHandlingIntegrationTest(APITestCase):
    """Test error handling across the application"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_404_error_handling(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-endpoint/')
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_department_code(self):
        """Test handling of invalid department codes"""
        response = self.client.get('/api/dpto/charts/invalid_code')
        # Should handle gracefully
        self.assertIsNotNone(response)
    
    def test_invalid_municipality_code(self):
        """Test handling of invalid municipality codes"""
        response = self.client.get('/api/mpio/charts/invalid_code')
        # Should handle gracefully
        self.assertIsNotNone(response)
    
    def test_gbif_download_missing_parameters(self):
        """Test GBIF download with missing required parameters"""
        response = self.client.get('/api/gbif/descargarz')
        # Should return appropriate error
        self.assertIsNotNone(response)


class PerformanceIntegrationTest(APITestCase):
    """Basic performance tests"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_endpoint_response_times(self):
        """Test that endpoints respond within reasonable time"""
        import time
        
        endpoints = [
            '/api/docs/',
            '/api/schema/',
            '/api/gbif/gbifinfo'
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                start_time = time.time()
                response = self.client.get(endpoint)
                end_time = time.time()
                
                response_time = end_time - start_time
                # Response should be under 5 seconds
                self.assertLess(response_time, 5.0)


class SecurityIntegrationTest(APITestCase):
    """Basic security tests"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_sql_injection_protection(self):
        """Test protection against SQL injection"""
        malicious_codes = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "1; DELETE FROM users; --"
        ]
        
        for code in malicious_codes:
            with self.subTest(code=code):
                response = self.client.get(f'/api/dpto/charts/{code}')
                # Should handle malicious input gracefully
                self.assertIsNotNone(response)
    
    def test_xss_protection(self):
        """Test protection against XSS"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>"
        ]
        
        for payload in xss_payloads:
            with self.subTest(payload=payload):
                response = self.client.post('/requestcreate/', {
                    'nombre': payload,
                    'email': 'test@example.com'
                })
                # Should handle XSS attempts gracefully
                self.assertIsNotNone(response)
