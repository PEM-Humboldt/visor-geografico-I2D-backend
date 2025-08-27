"""
Serializer tests for Visor I2D Backend
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from applications.user.serializers import SolicitudSerializer
from applications.dpto.serializers import dptoQueriesSerializer, dptoDangerSerializer
from applications.mupio.serializers import mpioQueriesSerializer, mpioDangerSerializer
from applications.gbif.serializers import gbifInfoSerializer
from unittest.mock import MagicMock


class SolicitudSerializerTest(TestCase):
    """Test cases for SolicitudSerializer"""
    
    def setUp(self):
        self.valid_data = {
            'entidad': 'Universidad Nacional',
            'nombre': 'Juan Pérez',
            'email': 'juan.perez@unal.edu.co',
            'observacion': 'Solicitud de datos para investigación'
        }
        self.invalid_data = {
            'entidad': 'x' * 50,  # Exceeds max_length
            'email': 'invalid-email'
        }
    
    def test_valid_serializer(self):
        """Test serializer with valid data"""
        serializer = SolicitudSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Test that all fields are included
        self.assertIn('entidad', serializer.validated_data)
        self.assertIn('nombre', serializer.validated_data)
        self.assertIn('email', serializer.validated_data)
        self.assertIn('observacion', serializer.validated_data)
    
    def test_serializer_fields(self):
        """Test that serializer includes all model fields"""
        serializer = SolicitudSerializer()
        expected_fields = ['id_solicitud', 'entidad', 'nombre', 'email', 'observacion']
        
        # Since fields="__all__", all model fields should be included
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_empty_data_serializer(self):
        """Test serializer with empty data"""
        serializer = SolicitudSerializer(data={})
        # Since all fields are nullable, empty data should be valid
        self.assertTrue(serializer.is_valid())


class DptoSerializersTest(TestCase):
    """Test cases for Department serializers"""
    
    def test_dpto_queries_serializer_structure(self):
        """Test dptoQueriesSerializer structure"""
        serializer = dptoQueriesSerializer()
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_dpto_danger_serializer_structure(self):
        """Test dptoDangerSerializer structure"""
        serializer = dptoDangerSerializer()
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_dpto_serializer_with_mock_data(self):
        """Test department serializer with mock data"""
        mock_instance = MagicMock()
        mock_instance.codigo = '05'
        mock_instance.tipo = 'especies'
        mock_instance.valor = 100
        
        serializer = dptoQueriesSerializer(mock_instance)
        # Test that serializer can handle the instance
        self.assertIsNotNone(serializer.data)


class MpioSerializersTest(TestCase):
    """Test cases for Municipality serializers"""
    
    def test_mpio_queries_serializer_structure(self):
        """Test mpioQueriesSerializer structure"""
        serializer = mpioQueriesSerializer()
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_mpio_danger_serializer_structure(self):
        """Test mpioDangerSerializer structure"""
        serializer = mpioDangerSerializer()
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_mpio_serializer_with_mock_data(self):
        """Test municipality serializer with mock data"""
        mock_instance = MagicMock()
        mock_instance.codigo = '05001'
        mock_instance.tipo = 'especies'
        mock_instance.valor = 150
        
        serializer = mpioQueriesSerializer(mock_instance)
        self.assertIsNotNone(serializer.data)


class GbifSerializerTest(TestCase):
    """Test cases for GBIF serializer"""
    
    def test_gbif_info_serializer_structure(self):
        """Test gbifInfoSerializer structure"""
        serializer = gbifInfoSerializer()
        self.assertTrue(hasattr(serializer, 'Meta'))
        self.assertEqual(serializer.Meta.fields, "__all__")
    
    def test_gbif_serializer_with_mock_data(self):
        """Test GBIF serializer with mock data"""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.species = 'Quercus humboldtii'
        mock_instance.latitude = 4.5981
        mock_instance.longitude = -74.0758
        
        serializer = gbifInfoSerializer(mock_instance)
        self.assertIsNotNone(serializer.data)


class SerializerIntegrationTest(APITestCase):
    """Integration tests for serializers"""
    
    def test_all_serializers_import_correctly(self):
        """Test that all serializers can be imported and instantiated"""
        serializers = [
            SolicitudSerializer,
            dptoQueriesSerializer,
            dptoDangerSerializer,
            mpioQueriesSerializer,
            mpioDangerSerializer,
            gbifInfoSerializer
        ]
        
        for serializer_class in serializers:
            # Test that serializer can be instantiated
            serializer = serializer_class()
            self.assertIsNotNone(serializer)
            
            # Test that it has Meta class
            self.assertTrue(hasattr(serializer, 'Meta'))
            
            # Test that it has fields attribute
            self.assertTrue(hasattr(serializer.Meta, 'fields'))
    
    def test_serializer_validation_methods(self):
        """Test common serializer validation methods"""
        serializer = SolicitudSerializer(data={})
        
        # Test validation methods exist
        self.assertTrue(hasattr(serializer, 'is_valid'))
        self.assertTrue(hasattr(serializer, 'validated_data'))
        self.assertTrue(hasattr(serializer, 'errors'))
        
        # Test validation
        is_valid = serializer.is_valid()
        self.assertIsInstance(is_valid, bool)
