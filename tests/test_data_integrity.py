"""
Data integrity tests for Visor I2D Backend
"""
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.exceptions import ValidationError
from applications.common.validators import (
    department_validator, municipality_validator, 
    biodiversity_validator, gbif_validator, user_request_validator
)


class DataIntegrityTestCase(TestCase):
    """Test data integrity and validation"""
    
    def test_department_code_validation(self):
        """Test Colombian department code validation"""
        # Valid department codes
        valid_codes = ['05', '11', '76', '25']
        for code in valid_codes:
            try:
                result = department_validator(code)
                self.assertEqual(result, code)
            except ValidationError:
                self.fail(f"Valid department code {code} failed validation")
        
        # Invalid department codes
        invalid_codes = ['00', '99', 'AB', '123', '5', '']
        for code in invalid_codes:
            with self.assertRaises(ValidationError):
                department_validator(code)
    
    def test_municipality_code_validation(self):
        """Test Colombian municipality code validation"""
        # Valid municipality codes
        valid_codes = ['05001', '11001', '76001', '25001']
        for code in valid_codes:
            try:
                result = municipality_validator(code)
                self.assertEqual(result, code)
            except ValidationError:
                self.fail(f"Valid municipality code {code} failed validation")
        
        # Invalid municipality codes
        invalid_codes = ['00001', '99999', 'ABCDE', '123', '05', '']
        for code in invalid_codes:
            with self.assertRaises(ValidationError):
                municipality_validator(code)
    
    def test_biodiversity_data_validation(self):
        """Test biodiversity data type validation"""
        # Valid data types
        valid_types = ['especies', 'registros', 'familias', 'amenazadas']
        for data_type in valid_types:
            try:
                result = biodiversity_validator.validate_data_type(data_type)
                self.assertEqual(result, data_type.lower())
            except ValidationError:
                self.fail(f"Valid data type {data_type} failed validation")
        
        # Invalid data types
        invalid_types = ['invalid', '', 123, None]
        for data_type in invalid_types:
            with self.assertRaises(ValidationError):
                biodiversity_validator.validate_data_type(data_type)
    
    def test_numeric_value_validation(self):
        """Test numeric value validation"""
        # Valid numeric values
        valid_values = [0, 1, 100, 1000, '50', '999']
        for value in valid_values:
            try:
                result = biodiversity_validator.validate_numeric_value(value)
                self.assertIsInstance(result, int)
                self.assertGreaterEqual(result, 0)
            except ValidationError:
                self.fail(f"Valid numeric value {value} failed validation")
        
        # Invalid numeric values
        invalid_values = [-1, 'abc', '', None, []]
        for value in invalid_values:
            with self.assertRaises(ValidationError):
                biodiversity_validator.validate_numeric_value(value)
    
    def test_species_name_validation(self):
        """Test scientific species name validation"""
        # Valid species names
        valid_names = [
            'Quercus humboldtii',
            'Espeletia grandiflora',
            'Panthera onca',
            'Ara macao'
        ]
        for name in valid_names:
            try:
                result = gbif_validator.validate_species_name(name)
                self.assertEqual(result, name)
            except ValidationError:
                self.fail(f"Valid species name {name} failed validation")
        
        # Invalid species names
        invalid_names = [
            'quercus humboldtii',  # lowercase genus
            'Quercus',  # missing species
            'QUERCUS HUMBOLDTII',  # all uppercase
            '',  # empty
            123  # not string
        ]
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                gbif_validator.validate_species_name(name)
    
    def test_coordinate_validation(self):
        """Test geographic coordinate validation"""
        # Valid Colombian coordinates
        valid_coords = [
            (4.7110, -74.0721),  # Bogotá
            (6.2442, -75.5812),  # Medellín
            (3.4516, -76.5320),  # Cali
            (10.9685, -74.7813)  # Barranquilla
        ]
        for lat, lon in valid_coords:
            try:
                result_lat, result_lon = gbif_validator.validate_coordinates(lat, lon)
                self.assertEqual(result_lat, lat)
                self.assertEqual(result_lon, lon)
            except ValidationError:
                self.fail(f"Valid coordinates ({lat}, {lon}) failed validation")
        
        # Invalid coordinates
        invalid_coords = [
            (50.0, -74.0),  # Outside Colombia (north)
            (-10.0, -74.0),  # Outside Colombia (south)
            (4.0, -50.0),  # Outside Colombia (east)
            (4.0, -90.0),  # Outside Colombia (west)
            ('abc', 'def'),  # Non-numeric
        ]
        for lat, lon in invalid_coords:
            with self.assertRaises(ValidationError):
                gbif_validator.validate_coordinates(lat, lon)
    
    def test_date_validation(self):
        """Test occurrence date validation"""
        # Valid dates
        valid_dates = [
            '2023-01-15',
            '2020/12/31',
            '15-06-2021',
            '01/01/2022'
        ]
        for date_str in valid_dates:
            try:
                result = gbif_validator.validate_date_format(date_str)
                self.assertIsNotNone(result)
            except ValidationError:
                self.fail(f"Valid date {date_str} failed validation")
        
        # Invalid dates
        invalid_dates = [
            '2025-01-01',  # Future date
            '1700-01-01',  # Too old
            'invalid-date',  # Invalid format
            '32/13/2023',  # Invalid day/month
        ]
        for date_str in invalid_dates:
            with self.assertRaises(ValidationError):
                gbif_validator.validate_date_format(date_str)
    
    def test_email_validation(self):
        """Test email format validation"""
        # Valid emails
        valid_emails = [
            'user@example.com',
            'test.email@university.edu.co',
            'researcher@humboldt.org.co'
        ]
        for email in valid_emails:
            try:
                result = user_request_validator.validate_email(email)
                self.assertEqual(result, email)
            except ValidationError:
                self.fail(f"Valid email {email} failed validation")
        
        # Invalid emails
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'user@',
            '',
            123
        ]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                user_request_validator.validate_email(email)
    
    def test_institution_validation(self):
        """Test institution name validation"""
        # Valid institutions
        valid_institutions = [
            'Universidad Nacional de Colombia',
            'Instituto Humboldt',
            'SINCHI'
        ]
        for institution in valid_institutions:
            try:
                result = user_request_validator.validate_institution(institution)
                self.assertEqual(result, institution)
            except ValidationError:
                self.fail(f"Valid institution {institution} failed validation")
        
        # Invalid institutions
        invalid_institutions = [
            '',  # Empty
            'A',  # Too short
            'A' * 201,  # Too long
            '<script>alert("xss")</script>',  # XSS attempt
            123  # Not string
        ]
        for institution in invalid_institutions:
            with self.assertRaises(ValidationError):
                user_request_validator.validate_institution(institution)
    
    def test_observation_validation(self):
        """Test observation text validation"""
        # Valid observations
        valid_observations = [
            'Solicitud de datos para investigación',
            'Necesito información sobre especies endémicas',
            ''  # Empty is allowed
        ]
        for observation in valid_observations:
            try:
                result = user_request_validator.validate_observation(observation)
                self.assertEqual(result, observation.strip())
            except ValidationError:
                self.fail(f"Valid observation failed validation")
        
        # Invalid observations
        invalid_observations = [
            'A' * 1001,  # Too long
            '<script>alert("xss")</script>',  # XSS attempt
            'DROP TABLE users;',  # SQL injection attempt
            123  # Not string
        ]
        for observation in invalid_observations:
            with self.assertRaises(ValidationError):
                user_request_validator.validate_observation(observation)


class DatabaseIntegrityTestCase(TestCase):
    """Test database integrity and constraints"""
    
    @patch('applications.user.models.Solicitud.objects')
    def test_solicitud_model_integrity(self, mock_solicitud):
        """Test Solicitud model data integrity"""
        # Test required fields
        mock_instance = MagicMock()
        mock_solicitud.create.return_value = mock_instance
        
        # Valid data
        valid_data = {
            'entidad': 'Universidad Nacional',
            'nombre': 'Juan Pérez',
            'email': 'juan@unal.edu.co',
            'observacion': 'Solicitud de datos'
        }
        
        try:
            # Validate each field
            user_request_validator.validate_institution(valid_data['entidad'])
            user_request_validator.validate_email(valid_data['email'])
            user_request_validator.validate_observation(valid_data['observacion'])
            
            # If all validations pass, the data is valid
            self.assertTrue(True)
        except ValidationError:
            self.fail("Valid solicitud data failed validation")
    
    @patch('applications.dpto.models.DptoQueries.objects')
    def test_dpto_queries_integrity(self, mock_queries):
        """Test DptoQueries model data integrity"""
        mock_instance = MagicMock()
        mock_instance.codigo = '05'
        mock_instance.tipo = 'especies'
        mock_instance.valor = 100
        mock_queries.filter.return_value = [mock_instance]
        
        # Validate department code
        try:
            department_validator(mock_instance.codigo)
            biodiversity_validator.validate_data_type(mock_instance.tipo)
            biodiversity_validator.validate_numeric_value(mock_instance.valor)
            self.assertTrue(True)
        except ValidationError:
            self.fail("Valid DptoQueries data failed validation")
    
    @patch('applications.mpio.models.MpioQueries.objects')
    def test_mpio_queries_integrity(self, mock_queries):
        """Test MpioQueries model data integrity"""
        mock_instance = MagicMock()
        mock_instance.codigo = '05001'
        mock_instance.tipo = 'registros'
        mock_instance.valor = 500
        mock_queries.filter.return_value = [mock_instance]
        
        # Validate municipality code
        try:
            municipality_validator(mock_instance.codigo)
            biodiversity_validator.validate_data_type(mock_instance.tipo)
            biodiversity_validator.validate_numeric_value(mock_instance.valor)
            self.assertTrue(True)
        except ValidationError:
            self.fail("Valid MpioQueries data failed validation")
    
    @patch('applications.gbif.models.gbifInfo.objects')
    def test_gbif_info_integrity(self, mock_gbif):
        """Test GBIF info model data integrity"""
        mock_instance = MagicMock()
        mock_instance.species = 'Quercus humboldtii'
        mock_instance.latitude = 4.7110
        mock_instance.longitude = -74.0721
        mock_instance.recorded_by = 'Researcher Name'
        mock_gbif.filter.return_value = [mock_instance]
        
        # Validate GBIF data
        try:
            gbif_validator.validate_species_name(mock_instance.species)
            gbif_validator.validate_coordinates(
                mock_instance.latitude, 
                mock_instance.longitude
            )
            self.assertTrue(True)
        except ValidationError:
            self.fail("Valid GBIF data failed validation")


class SecurityIntegrityTestCase(TestCase):
    """Test security-related data integrity"""
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention in validators"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "UNION SELECT * FROM users",
            "'; DELETE FROM solicitudes; --"
        ]
        
        for malicious_input in malicious_inputs:
            # Test department validator
            with self.assertRaises(ValidationError):
                department_validator(malicious_input)
            
            # Test institution validator
            with self.assertRaises(ValidationError):
                user_request_validator.validate_institution(malicious_input)
            
            # Test observation validator
            with self.assertRaises(ValidationError):
                user_request_validator.validate_observation(malicious_input)
    
    def test_xss_prevention(self):
        """Test XSS prevention in validators"""
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "data:text/html,<script>alert('xss')</script>"
        ]
        
        for xss_input in xss_inputs:
            # Test institution validator
            with self.assertRaises(ValidationError):
                user_request_validator.validate_institution(xss_input)
            
            # Test observation validator
            with self.assertRaises(ValidationError):
                user_request_validator.validate_observation(xss_input)
    
    def test_data_size_limits(self):
        """Test data size limits"""
        # Test institution name length limit
        long_institution = 'A' * 201
        with self.assertRaises(ValidationError):
            user_request_validator.validate_institution(long_institution)
        
        # Test observation length limit
        long_observation = 'A' * 1001
        with self.assertRaises(ValidationError):
            user_request_validator.validate_observation(long_observation)
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        # Test whitespace trimming
        institution_with_spaces = '  Universidad Nacional  '
        result = user_request_validator.validate_institution(institution_with_spaces)
        self.assertEqual(result, 'Universidad Nacional')
        
        observation_with_spaces = '  Solicitud de datos  '
        result = user_request_validator.validate_observation(observation_with_spaces)
        self.assertEqual(result, 'Solicitud de datos')
