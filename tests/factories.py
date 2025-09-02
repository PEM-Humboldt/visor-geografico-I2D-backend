"""
Factory classes for creating test data
"""
import factory
from faker import Faker
from applications.user.models import Solicitud

fake = Faker()


class SolicitudFactory(factory.Factory):
    """Factory for creating Solicitud test instances"""
    
    class Meta:
        model = Solicitud
    
    entidad = factory.LazyFunction(lambda: fake.company())
    nombre = factory.LazyFunction(lambda: fake.name())
    email = factory.LazyFunction(lambda: fake.email())
    observacion = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))


# Mock data factories for unmanaged models
class MockDptoQueriesFactory:
    """Mock factory for DptoQueries data"""
    
    @staticmethod
    def create(**kwargs):
        from unittest.mock import MagicMock
        mock_obj = MagicMock()
        mock_obj.codigo = kwargs.get('codigo', '05')
        mock_obj.tipo = kwargs.get('tipo', 'especies')
        mock_obj.valor = kwargs.get('valor', fake.random_int(min=1, max=1000))
        mock_obj.nombre = kwargs.get('nombre', fake.state())
        return mock_obj


class MockMpioQueriesFactory:
    """Mock factory for MpioQueries data"""
    
    @staticmethod
    def create(**kwargs):
        from unittest.mock import MagicMock
        mock_obj = MagicMock()
        mock_obj.codigo = kwargs.get('codigo', '05001')
        mock_obj.tipo = kwargs.get('tipo', 'especies')
        mock_obj.valor = kwargs.get('valor', fake.random_int(min=1, max=500))
        mock_obj.nombre = kwargs.get('nombre', fake.city())
        return mock_obj


class MockGbifInfoFactory:
    """Mock factory for GBIF data"""
    
    @staticmethod
    def create(**kwargs):
        from unittest.mock import MagicMock
        mock_obj = MagicMock()
        mock_obj.id = kwargs.get('id', fake.random_int(min=1, max=10000))
        mock_obj.species = kwargs.get('species', fake.word() + ' ' + fake.word())
        mock_obj.latitude = kwargs.get('latitude', fake.latitude())
        mock_obj.longitude = kwargs.get('longitude', fake.longitude())
        mock_obj.recorded_by = kwargs.get('recorded_by', fake.name())
        mock_obj.occurrence_date = kwargs.get('occurrence_date', fake.date())
        return mock_obj
