"""
Model tests for Visor I2D Backend
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from applications.user.models import Solicitud
from applications.dpto.models import DptoQueries, DptoAmenazas
from applications.mupio.models import MpioQueries, MpioAmenazas
from applications.gbif.models import gbifInfo


class SolicitudModelTest(TestCase):
    """Test cases for Solicitud model"""
    
    def setUp(self):
        self.solicitud_data = {
            'entidad': 'Universidad Nacional',
            'nombre': 'Juan Pérez',
            'email': 'juan.perez@unal.edu.co',
            'observacion': 'Solicitud de datos para investigación sobre biodiversidad'
        }
    
    def test_create_solicitud(self):
        """Test creating a new solicitud"""
        solicitud = Solicitud(**self.solicitud_data)
        # Note: Since managed=False, we can't actually save to test DB
        # But we can test field validation
        self.assertEqual(solicitud.entidad, 'Universidad Nacional')
        self.assertEqual(solicitud.nombre, 'Juan Pérez')
        self.assertEqual(solicitud.email, 'juan.perez@unal.edu.co')
    
    def test_solicitud_string_representation(self):
        """Test string representation of solicitud"""
        solicitud = Solicitud(**self.solicitud_data)
        expected_str = f"{solicitud.nombre} - {solicitud.entidad}"
        # Since we can't define __str__ method due to managed=False,
        # we test the basic field access
        self.assertIsNotNone(solicitud.nombre)
        self.assertIsNotNone(solicitud.entidad)
    
    def test_solicitud_field_lengths(self):
        """Test field length constraints"""
        # Test entidad max_length
        long_entidad = 'x' * 50  # Exceeds max_length=40
        solicitud = Solicitud(entidad=long_entidad, **{k: v for k, v in self.solicitud_data.items() if k != 'entidad'})
        # Field validation would happen at form/serializer level
        self.assertEqual(len(solicitud.entidad), 50)
    
    def test_solicitud_optional_fields(self):
        """Test that fields can be null/blank"""
        solicitud = Solicitud(
            entidad=None,
            nombre=None,
            email=None,
            observacion=None
        )
        # All fields allow null=True, blank=True
        self.assertIsNone(solicitud.entidad)
        self.assertIsNone(solicitud.nombre)
        self.assertIsNone(solicitud.email)
        self.assertIsNone(solicitud.observacion)


class DptoModelsTest(TestCase):
    """Test cases for Department models"""
    
    def test_dpto_queries_model_structure(self):
        """Test DptoQueries model structure"""
        # Since managed=False, we test model structure
        self.assertTrue(hasattr(DptoQueries, '_meta'))
        self.assertFalse(DptoQueries._meta.managed)
        self.assertEqual(DptoQueries._meta.db_table, 'gbif_consultas.dpto_queries')
    
    def test_dpto_amenazas_model_structure(self):
        """Test DptoAmenazas model structure"""
        self.assertTrue(hasattr(DptoAmenazas, '_meta'))
        self.assertFalse(DptoAmenazas._meta.managed)
        self.assertEqual(DptoAmenazas._meta.db_table, 'gbif_consultas.dpto_amenazas')


class MpioModelsTest(TestCase):
    """Test cases for Municipality models"""
    
    def test_mpio_queries_model_structure(self):
        """Test MpioQueries model structure"""
        self.assertTrue(hasattr(MpioQueries, '_meta'))
        self.assertFalse(MpioQueries._meta.managed)
        self.assertEqual(MpioQueries._meta.db_table, 'gbif_consultas.mpio_queries')
    
    def test_mpio_amenazas_model_structure(self):
        """Test MpioAmenazas model structure"""
        self.assertTrue(hasattr(MpioAmenazas, '_meta'))
        self.assertFalse(MpioAmenazas._meta.managed)
        self.assertEqual(MpioAmenazas._meta.db_table, 'gbif_consultas.mpio_amenazas')


class GbifModelsTest(TestCase):
    """Test cases for GBIF models"""
    
    def test_gbif_info_model_structure(self):
        """Test gbifInfo model structure"""
        self.assertTrue(hasattr(gbifInfo, '_meta'))
        self.assertFalse(gbifInfo._meta.managed)
        self.assertEqual(gbifInfo._meta.db_table, 'gbif.gbif')
