"""
Comprehensive input validation utilities for Visor I2D Backend
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


class ColombianDepartmentValidator:
    """Validator for Colombian department codes"""
    
    VALID_DEPARTMENTS = {
        '05': 'Antioquia', '08': 'Atlántico', '11': 'Bogotá D.C.', '13': 'Bolívar',
        '15': 'Boyacá', '17': 'Caldas', '18': 'Caquetá', '19': 'Cauca',
        '20': 'Cesar', '23': 'Córdoba', '25': 'Cundinamarca', '27': 'Chocó',
        '41': 'Huila', '44': 'La Guajira', '47': 'Magdalena', '50': 'Meta',
        '52': 'Nariño', '54': 'Norte de Santander', '63': 'Quindío', '66': 'Risaralda',
        '68': 'Santander', '70': 'Sucre', '73': 'Tolima', '76': 'Valle del Cauca',
        '81': 'Arauca', '85': 'Casanare', '86': 'Putumayo', '88': 'San Andrés',
        '91': 'Amazonas', '94': 'Guainía', '95': 'Guaviare', '97': 'Vaichada',
        '99': 'Vichada'
    }
    
    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError('Department code must be a string')
        
        if len(value) != 2:
            raise ValidationError('Department code must be exactly 2 digits')
        
        if not value.isdigit():
            raise ValidationError('Department code must contain only digits')
        
        if value not in self.VALID_DEPARTMENTS:
            raise ValidationError(f'Invalid department code: {value}')
        
        return value


class ColombianMunicipalityValidator:
    """Validator for Colombian municipality codes"""
    
    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError('Municipality code must be a string')
        
        if len(value) != 5:
            raise ValidationError('Municipality code must be exactly 5 digits')
        
        if not value.isdigit():
            raise ValidationError('Municipality code must contain only digits')
        
        # Validate department part (first 2 digits)
        dept_code = value[:2]
        dept_validator = ColombianDepartmentValidator()
        try:
            dept_validator(dept_code)
        except ValidationError:
            raise ValidationError(f'Invalid department in municipality code: {dept_code}')
        
        return value


class BiodiversityDataValidator:
    """Validator for biodiversity data parameters"""
    
    VALID_DATA_TYPES = [
        'especies', 'registros', 'familias', 'generos', 'ordenes',
        'amenazadas', 'endemicas', 'migratorias', 'invasoras'
    ]
    
    def validate_data_type(self, value):
        """Validate biodiversity data type"""
        if not isinstance(value, str):
            raise ValidationError('Data type must be a string')
        
        if value.lower() not in self.VALID_DATA_TYPES:
            raise ValidationError(
                f'Invalid data type: {value}. Valid types: {", ".join(self.VALID_DATA_TYPES)}'
            )
        
        return value.lower()
    
    def validate_numeric_value(self, value, min_value=0, max_value=None):
        """Validate numeric biodiversity values"""
        try:
            numeric_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError('Value must be a valid integer')
        
        if numeric_value < min_value:
            raise ValidationError(f'Value must be at least {min_value}')
        
        if max_value and numeric_value > max_value:
            raise ValidationError(f'Value must not exceed {max_value}')
        
        return numeric_value


class GBIFDataValidator:
    """Validator for GBIF occurrence data"""
    
    def validate_species_name(self, value):
        """Validate scientific species name format"""
        if not isinstance(value, str):
            raise ValidationError('Species name must be a string')
        
        # Basic scientific name pattern: Genus species
        pattern = r'^[A-Z][a-z]+ [a-z]+( [a-z]+)*$'
        if not re.match(pattern, value.strip()):
            raise ValidationError(
                'Species name must follow scientific nomenclature: "Genus species"'
            )
        
        return value.strip()
    
    def validate_coordinates(self, latitude, longitude):
        """Validate geographic coordinates"""
        try:
            lat = float(latitude)
            lon = float(longitude)
        except (ValueError, TypeError):
            raise ValidationError('Coordinates must be valid numbers')
        
        # Colombia approximate bounds
        if not (-4.5 <= lat <= 16.0):
            raise ValidationError('Latitude must be within Colombian territory (-4.5 to 16.0)')
        
        if not (-82.0 <= lon <= -66.0):
            raise ValidationError('Longitude must be within Colombian territory (-82.0 to -66.0)')
        
        return lat, lon
    
    def validate_date_format(self, value):
        """Validate occurrence date format"""
        from datetime import datetime
        
        if not value:
            return None
        
        # Try multiple date formats
        date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(str(value), fmt)
                # Check if date is reasonable (not in future, not too old)
                current_year = datetime.now().year
                if parsed_date.year > current_year:
                    raise ValidationError('Date cannot be in the future')
                if parsed_date.year < 1800:
                    raise ValidationError('Date cannot be before 1800')
                return parsed_date.date()
            except ValueError:
                continue
        
        raise ValidationError(
            f'Invalid date format: {value}. Use YYYY-MM-DD, DD/MM/YYYY, or similar'
        )


class UserRequestValidator:
    """Validator for user data requests"""
    
    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise ValidationError('Invalid email format')
    
    def validate_institution(self, value):
        """Validate institution name"""
        if not isinstance(value, str):
            raise ValidationError('Institution name must be a string')
        
        if len(value.strip()) < 2:
            raise ValidationError('Institution name must be at least 2 characters')
        
        if len(value.strip()) > 200:
            raise ValidationError('Institution name must not exceed 200 characters')
        
        # Check for potentially malicious content
        dangerous_patterns = ['<script', 'javascript:', 'data:', 'vbscript:']
        value_lower = value.lower()
        for pattern in dangerous_patterns:
            if pattern in value_lower:
                raise ValidationError('Institution name contains invalid content')
        
        return value.strip()
    
    def validate_observation(self, value):
        """Validate observation text"""
        if not isinstance(value, str):
            raise ValidationError('Observation must be a string')
        
        if len(value.strip()) > 1000:
            raise ValidationError('Observation must not exceed 1000 characters')
        
        # Check for potentially malicious content
        dangerous_patterns = ['<script', 'javascript:', 'data:', 'vbscript:', 'DROP TABLE', 'DELETE FROM']
        value_lower = value.lower()
        for pattern in dangerous_patterns:
            if pattern in value_lower:
                raise ValidationError('Observation contains invalid content')
        
        return value.strip()


# Validator instances for reuse
department_validator = ColombianDepartmentValidator()
municipality_validator = ColombianMunicipalityValidator()
biodiversity_validator = BiodiversityDataValidator()
gbif_validator = GBIFDataValidator()
user_request_validator = UserRequestValidator()


class CustomPasswordValidator:
    """Enhanced password validator for production security"""
    
    def validate(self, password, user=None):
        """Validate password strength"""
        errors = []
        
        # Check minimum length
        if len(password) < 12:
            errors.append('Password must be at least 12 characters long')
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter')
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter')
        
        # Check for digit
        if not re.search(r'\d', password):
            errors.append('Password must contain at least one digit')
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password must contain at least one special character')
        
        # Check for common patterns
        common_patterns = ['123', 'abc', 'password', 'admin', 'qwerty']
        password_lower = password.lower()
        for pattern in common_patterns:
            if pattern in password_lower:
                errors.append(f'Password cannot contain common pattern: {pattern}')
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return (
            "Your password must contain at least 12 characters, including uppercase, "
            "lowercase, digits, and special characters."
        )


def validate_query_parameters(params_dict, required_params=None, optional_params=None):
    """
    Validate query parameters for API endpoints
    
    Args:
        params_dict: Dictionary of parameters to validate
        required_params: List of required parameter names
        optional_params: List of optional parameter names
    
    Returns:
        dict: Validated and cleaned parameters
    
    Raises:
        ValidationError: If validation fails
    """
    validated_params = {}
    errors = []
    
    # Check required parameters
    if required_params:
        for param in required_params:
            if param not in params_dict or not params_dict[param]:
                errors.append(f'Required parameter missing: {param}')
            else:
                validated_params[param] = params_dict[param]
    
    # Validate optional parameters
    if optional_params:
        for param in optional_params:
            if param in params_dict and params_dict[param]:
                validated_params[param] = params_dict[param]
    
    # Check for unexpected parameters
    allowed_params = set((required_params or []) + (optional_params or []))
    unexpected_params = set(params_dict.keys()) - allowed_params
    if unexpected_params:
        errors.append(f'Unexpected parameters: {", ".join(unexpected_params)}')
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return validated_params


def sanitize_input(value, max_length=None, allow_html=False):
    """
    Sanitize user input to prevent XSS and injection attacks
    
    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length
        allow_html: Whether to allow HTML tags
    
    Returns:
        str: Sanitized input
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Trim whitespace
    value = value.strip()
    
    # Check length
    if max_length and len(value) > max_length:
        raise ValidationError(f'Input exceeds maximum length of {max_length} characters')
    
    # Remove or escape HTML if not allowed
    if not allow_html:
        import html
        value = html.escape(value)
    
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'data:',
        r'vbscript:',
        r'on\w+\s*=',
    ]
    
    for pattern in dangerous_patterns:
        value = re.sub(pattern, '', value, flags=re.IGNORECASE | re.DOTALL)
    
    return value
