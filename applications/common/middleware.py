"""
Data quality and validation middleware for Visor I2D Backend
"""
import json
import logging
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


logger = logging.getLogger(__name__)


class DataQualityMiddleware(MiddlewareMixin):
    """Middleware for data quality checks and validation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Process incoming requests for data quality"""
        
        # Skip validation for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
        
        # Validate request size
        if hasattr(request, 'META') and 'CONTENT_LENGTH' in request.META:
            try:
                content_length = int(request.META['CONTENT_LENGTH'])
                if content_length > 10 * 1024 * 1024:  # 10MB limit
                    return JsonResponse({
                        'error': 'Request too large',
                        'message': 'Request size exceeds 10MB limit',
                        'code': 'REQUEST_TOO_LARGE'
                    }, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            except (ValueError, TypeError):
                pass
        
        # Validate JSON payload for POST/PUT requests
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                if hasattr(request, 'body') and request.body:
                    json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return JsonResponse({
                    'error': 'Invalid JSON',
                    'message': f'Request body contains invalid JSON: {str(e)}',
                    'code': 'INVALID_JSON'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log suspicious patterns
        self._check_suspicious_patterns(request)
        
        return None
    
    def process_response(self, request, response):
        """Process outgoing responses for data quality"""
        
        # Add data quality headers
        response['X-Data-Quality-Check'] = 'enabled'
        response['X-Validation-Version'] = '1.0'
        
        # Log response metrics
        if hasattr(response, 'status_code'):
            if response.status_code >= 400:
                logger.warning(f"Error response {response.status_code} for {request.path}")
        
        return response
    
    def _check_suspicious_patterns(self, request):
        """Check for suspicious patterns in requests"""
        suspicious_patterns = [
            'DROP TABLE', 'DELETE FROM', 'INSERT INTO', 'UPDATE SET',
            '<script', 'javascript:', 'data:', 'vbscript:',
            'UNION SELECT', 'OR 1=1', "'; --", '" OR "',
            'eval(', 'exec(', 'system(', 'shell_exec'
        ]
        
        # Check URL parameters
        query_string = request.META.get('QUERY_STRING', '').lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in query_string:
                logger.warning(f"Suspicious pattern '{pattern}' detected in query: {request.path}?{query_string}")
                break
        
        # Check POST data
        if request.method == 'POST' and hasattr(request, 'body'):
            try:
                body_str = request.body.decode('utf-8').lower()
                for pattern in suspicious_patterns:
                    if pattern.lower() in body_str:
                        logger.warning(f"Suspicious pattern '{pattern}' detected in POST body for {request.path}")
                        break
            except UnicodeDecodeError:
                pass


class ErrorHandlingMiddleware(MiddlewareMixin):
    """Enhanced error handling middleware with structured responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_exception(self, request, exception):
        """Process exceptions with structured error responses"""
        
        # Handle validation errors
        if isinstance(exception, ValidationError):
            error_response = {
                'error': 'Validation Error',
                'message': str(exception),
                'code': 'VALIDATION_ERROR',
                'timestamp': self._get_timestamp(),
                'path': request.path
            }
            
            if hasattr(exception, 'error_dict'):
                error_response['details'] = exception.error_dict
            elif hasattr(exception, 'error_list'):
                error_response['details'] = [str(error) for error in exception.error_list]
            
            logger.error(f"Validation error on {request.path}: {str(exception)}")
            return JsonResponse(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle database errors
        if 'database' in str(type(exception)).lower():
            error_response = {
                'error': 'Database Error',
                'message': 'A database error occurred. Please try again later.',
                'code': 'DATABASE_ERROR',
                'timestamp': self._get_timestamp(),
                'path': request.path
            }
            
            logger.error(f"Database error on {request.path}: {str(exception)}")
            return JsonResponse(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Handle permission errors
        if 'permission' in str(type(exception)).lower():
            error_response = {
                'error': 'Permission Denied',
                'message': 'You do not have permission to access this resource.',
                'code': 'PERMISSION_DENIED',
                'timestamp': self._get_timestamp(),
                'path': request.path
            }
            
            logger.warning(f"Permission denied on {request.path}: {str(exception)}")
            return JsonResponse(error_response, status=status.HTTP_403_FORBIDDEN)
        
        # Log unexpected errors
        logger.error(f"Unexpected error on {request.path}: {str(exception)}", exc_info=True)
        
        return None
    
    def _get_timestamp(self):
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()


class APIVersioningMiddleware(MiddlewareMixin):
    """Middleware for API versioning and deprecation warnings"""
    
    CURRENT_VERSION = 'v1'
    SUPPORTED_VERSIONS = ['v1']
    DEPRECATED_VERSIONS = []
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Process API version from request"""
        
        # Skip non-API requests
        if not request.path.startswith('/api/'):
            return None
        
        # Extract version from URL or headers
        api_version = self._extract_version(request)
        
        # Set version in request
        request.api_version = api_version
        
        # Check if version is supported
        if api_version not in self.SUPPORTED_VERSIONS:
            return JsonResponse({
                'error': 'Unsupported API Version',
                'message': f'API version {api_version} is not supported',
                'supported_versions': self.SUPPORTED_VERSIONS,
                'current_version': self.CURRENT_VERSION,
                'code': 'UNSUPPORTED_VERSION'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return None
    
    def process_response(self, request, response):
        """Add version headers to response"""
        
        if hasattr(request, 'api_version'):
            response['X-API-Version'] = request.api_version
            response['X-API-Current-Version'] = self.CURRENT_VERSION
            
            # Add deprecation warning if needed
            if request.api_version in self.DEPRECATED_VERSIONS:
                response['X-API-Deprecation-Warning'] = f'API version {request.api_version} is deprecated'
                response['Warning'] = f'299 - "API version {request.api_version} is deprecated"'
        
        return response
    
    def _extract_version(self, request):
        """Extract API version from request"""
        
        # Check Accept header
        accept_header = request.META.get('HTTP_ACCEPT', '')
        if 'application/vnd.humboldt.v' in accept_header:
            import re
            match = re.search(r'application/vnd\.humboldt\.v(\d+)', accept_header)
            if match:
                return f'v{match.group(1)}'
        
        # Check custom header
        version_header = request.META.get('HTTP_X_API_VERSION', '')
        if version_header:
            return version_header
        
        # Check URL path
        path_parts = request.path.strip('/').split('/')
        if len(path_parts) > 1 and path_parts[1].startswith('v'):
            return path_parts[1]
        
        # Default to current version
        return self.CURRENT_VERSION


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for comprehensive request logging"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """Log incoming requests"""
        
        # Skip static files and admin
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None
        
        request.start_time = self._get_current_time()
        
        log_data = {
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'remote_addr': self._get_client_ip(request),
            'timestamp': request.start_time.isoformat()
        }
        
        logger.info(f"Request: {json.dumps(log_data)}")
        
        return None
    
    def process_response(self, request, response):
        """Log response details"""
        
        if hasattr(request, 'start_time'):
            end_time = self._get_current_time()
            duration = (end_time - request.start_time).total_seconds() * 1000  # milliseconds
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration, 2),
                'response_size': len(response.content) if hasattr(response, 'content') else 0
            }
            
            if response.status_code >= 400:
                logger.warning(f"Response: {json.dumps(log_data)}")
            else:
                logger.info(f"Response: {json.dumps(log_data)}")
        
        return response
    
    def _get_current_time(self):
        """Get current datetime"""
        from datetime import datetime
        return datetime.now()
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
