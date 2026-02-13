"""
Enhanced serializers with comprehensive validation for Visor I2D Backend
"""
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .validators import (
    department_validator, municipality_validator, 
    biodiversity_validator, gbif_validator, user_request_validator
)


class ValidatedModelSerializer(serializers.ModelSerializer):
    """Base serializer with enhanced validation"""
    
    def validate(self, attrs):
        """Enhanced validation with custom validators"""
        attrs = super().validate(attrs)
        
        # Apply custom validation logic
        self.apply_custom_validation(attrs)
        
        return attrs
    
    def apply_custom_validation(self, attrs):
        """Override in subclasses for custom validation"""
        pass
    
    def to_internal_value(self, data):
        """Enhanced data conversion with validation"""
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            # Convert to structured error format
            raise serializers.ValidationError({
                'validation_errors': e.detail,
                'error_code': 'VALIDATION_FAILED',
                'message': 'Data validation failed'
            })


class EnhancedSolicitudSerializer(ValidatedModelSerializer):
    """Enhanced Solicitud serializer with comprehensive validation"""
    
    class Meta:
        from applications.user.models import Solicitud
        model = Solicitud
        fields = ['entidad', 'nombre', 'email', 'observacion']
    
    def apply_custom_validation(self, attrs):
        """Apply custom validation for Solicitud"""
        if 'entidad' in attrs:
            attrs['entidad'] = user_request_validator.validate_institution(attrs['entidad'])
        
        if 'email' in attrs:
            attrs['email'] = user_request_validator.validate_email(attrs['email'])
        
        if 'observacion' in attrs:
            attrs['observacion'] = user_request_validator.validate_observation(attrs['observacion'])
        
        # Validate nombre (similar to institution but for person names)
        if 'nombre' in attrs:
            if not isinstance(attrs['nombre'], str) or len(attrs['nombre'].strip()) < 2:
                raise serializers.ValidationError('Name must be at least 2 characters')
            if len(attrs['nombre'].strip()) > 100:
                raise serializers.ValidationError('Name must not exceed 100 characters')
            attrs['nombre'] = attrs['nombre'].strip()


class EnhancedDptoQueriesSerializer(ValidatedModelSerializer):
    """Enhanced DptoQueries serializer with validation"""
    
    codigo = serializers.CharField(max_length=2)
    tipo = serializers.CharField(max_length=50)
    valor = serializers.IntegerField(min_value=0)
    
    class Meta:
        from applications.dpto.models import DptoQueries
        model = DptoQueries
        fields = ['codigo', 'tipo', 'valor', 'nombre']
    
    def apply_custom_validation(self, attrs):
        """Apply custom validation for DptoQueries"""
        if 'codigo' in attrs:
            attrs['codigo'] = department_validator(attrs['codigo'])
        
        if 'tipo' in attrs:
            attrs['tipo'] = biodiversity_validator.validate_data_type(attrs['tipo'])
        
        if 'valor' in attrs:
            attrs['valor'] = biodiversity_validator.validate_numeric_value(attrs['valor'])


class EnhancedMpioQueriesSerializer(ValidatedModelSerializer):
    """Enhanced MpioQueries serializer with validation"""
    
    codigo = serializers.CharField(max_length=5)
    tipo = serializers.CharField(max_length=50)
    valor = serializers.IntegerField(min_value=0)
    
    class Meta:
        from applications.mpio.models import MpioQueries
        model = MpioQueries
        fields = ['codigo', 'tipo', 'valor', 'nombre']
    
    def apply_custom_validation(self, attrs):
        """Apply custom validation for MpioQueries"""
        if 'codigo' in attrs:
            attrs['codigo'] = municipality_validator(attrs['codigo'])
        
        if 'tipo' in attrs:
            attrs['tipo'] = biodiversity_validator.validate_data_type(attrs['tipo'])
        
        if 'valor' in attrs:
            attrs['valor'] = biodiversity_validator.validate_numeric_value(attrs['valor'])


class EnhancedGbifInfoSerializer(ValidatedModelSerializer):
    """Enhanced GBIF info serializer with validation"""
    
    species = serializers.CharField(max_length=200)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    occurrence_date = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        from applications.gbif.models import gbifInfo
        model = gbifInfo
        fields = ['id', 'species', 'latitude', 'longitude', 'recorded_by', 'occurrence_date']
    
    def apply_custom_validation(self, attrs):
        """Apply custom validation for GBIF data"""
        if 'species' in attrs:
            attrs['species'] = gbif_validator.validate_species_name(attrs['species'])
        
        if 'latitude' in attrs and 'longitude' in attrs:
            lat, lon = gbif_validator.validate_coordinates(
                attrs['latitude'], attrs['longitude']
            )
            attrs['latitude'] = lat
            attrs['longitude'] = lon
        
        if 'occurrence_date' in attrs and attrs['occurrence_date']:
            attrs['occurrence_date'] = gbif_validator.validate_date_format(attrs['occurrence_date'])


class APIResponseSerializer(serializers.Serializer):
    """Standardized API response serializer"""
    
    success = serializers.BooleanField(default=True)
    data = serializers.JSONField(required=False)
    message = serializers.CharField(required=False)
    errors = serializers.JSONField(required=False)
    metadata = serializers.JSONField(required=False)
    
    def create(self, validated_data):
        """Create standardized response"""
        return {
            'success': validated_data.get('success', True),
            'data': validated_data.get('data'),
            'message': validated_data.get('message'),
            'errors': validated_data.get('errors'),
            'metadata': {
                'timestamp': self._get_timestamp(),
                'version': 'v1',
                **validated_data.get('metadata', {})
            }
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for standardized error responses"""
    
    success = serializers.BooleanField(default=False)
    error = serializers.CharField()
    message = serializers.CharField()
    code = serializers.CharField()
    details = serializers.JSONField(required=False)
    timestamp = serializers.CharField()  # Changed to CharField for ISO string
    path = serializers.CharField()
    
    def create(self, validated_data):
        """Create standardized error response"""
        from datetime import datetime
        return {
            'success': False,
            'error': validated_data['error'],
            'message': validated_data['message'],
            'code': validated_data['code'],
            'details': validated_data.get('details'),
            'timestamp': validated_data.get('timestamp', datetime.now().isoformat()),
            'path': validated_data['path']
        }


class SpatialQuerySerializer(serializers.Serializer):
    """Serializer for spatial query parameters"""
    
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius_km = serializers.FloatField(default=10, min_value=0.1, max_value=100)
    
    def validate(self, attrs):
        """Validate spatial query parameters"""
        from .spatial import spatial_validator
        
        try:
            # Validate coordinates
            point = spatial_validator.validate_coordinates(
                attrs['latitude'], attrs['longitude']
            )
            attrs['validated_point'] = point
        except DjangoValidationError as e:
            raise serializers.ValidationError({'coordinates': str(e)})
        
        return attrs


class BulkOperationSerializer(serializers.Serializer):
    """Serializer for bulk operations"""
    
    operation = serializers.ChoiceField(choices=['create', 'update', 'delete'])
    data = serializers.ListField(child=serializers.JSONField())
    batch_size = serializers.IntegerField(default=100, min_value=1, max_value=1000)
    
    def validate_data(self, value):
        """Validate bulk data"""
        if not value:
            raise serializers.ValidationError('Data list cannot be empty')
        
        if len(value) > 1000:
            raise serializers.ValidationError('Bulk operations limited to 1000 items')
        
        return value


class DataQualityReportSerializer(serializers.Serializer):
    """Serializer for data quality reports"""
    
    total_records = serializers.IntegerField()
    valid_records = serializers.IntegerField()
    invalid_records = serializers.IntegerField()
    validation_errors = serializers.JSONField()
    quality_score = serializers.FloatField(min_value=0.0, max_value=100.0)
    
    def create(self, validated_data):
        """Create data quality report"""
        total = validated_data['total_records']
        valid = validated_data['valid_records']
        
        quality_score = (valid / total * 100) if total > 0 else 0
        
        return {
            **validated_data,
            'quality_score': round(quality_score, 2),
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
