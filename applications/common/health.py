"""
Comprehensive health check system for Visor I2D Backend
"""
import logging
import time
import os
import shutil
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status

logger = logging.getLogger(__name__)


class HealthCheckService:
    """Service for comprehensive health checks"""
    
    def __init__(self):
        self.checks = {
            'database': self._check_database,
            'cache': self._check_cache,
            'disk_space': self._check_disk_space,
            'memory': self._check_memory,
            'cpu': self._check_cpu,
            'external_apis': self._check_external_apis,
        }
    
    def run_all_checks(self):
        """Run all health checks and return results"""
        results = {
            'status': 'healthy',
            'timestamp': time.time(),
            'checks': {},
            'summary': {
                'total': len(self.checks),
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        
        for check_name, check_func in self.checks.items():
            try:
                check_result = check_func()
                results['checks'][check_name] = check_result
                
                if check_result['status'] == 'healthy':
                    results['summary']['passed'] += 1
                elif check_result['status'] == 'warning':
                    results['summary']['warnings'] += 1
                else:
                    results['summary']['failed'] += 1
                    results['status'] = 'unhealthy'
                    
            except Exception as e:
                logger.error(f"Health check {check_name} failed: {str(e)}")
                results['checks'][check_name] = {
                    'status': 'error',
                    'message': f'Check failed: {str(e)}',
                    'timestamp': time.time()
                }
                results['summary']['failed'] += 1
                results['status'] = 'unhealthy'
        
        return results
    
    def _check_database(self):
        """Check database connectivity and performance"""
        start_time = time.time()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            # Check connection pool
            db_connections = len(connection.queries)
            
            response_time = (time.time() - start_time) * 1000  # milliseconds
            
            status_level = 'healthy'
            message = 'Database is accessible'
            
            if response_time > 1000:  # 1 second
                status_level = 'warning'
                message = f'Database response time is high: {response_time:.2f}ms'
            elif response_time > 5000:  # 5 seconds
                status_level = 'unhealthy'
                message = f'Database response time is critical: {response_time:.2f}ms'
            
            return {
                'status': status_level,
                'message': message,
                'response_time_ms': round(response_time, 2),
                'connection_count': db_connections,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}',
                'timestamp': time.time()
            }
    
    def _check_cache(self):
        """Check cache system (Redis if configured)"""
        try:
            # Test cache write/read
            test_key = 'health_check_test'
            test_value = str(time.time())
            
            cache.set(test_key, test_value, 30)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                cache.delete(test_key)
                return {
                    'status': 'healthy',
                    'message': 'Cache is working correctly',
                    'timestamp': time.time()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': 'Cache read/write test failed',
                    'timestamp': time.time()
                }
                
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'Cache check failed: {str(e)}',
                'timestamp': time.time()
            }
    
    def _check_disk_space(self):
        """Check available disk space"""
        try:
            disk_usage = shutil.disk_usage('/')
            free_percent = (disk_usage.free / disk_usage.total) * 100
            
            status_level = 'healthy'
            message = f'Disk space: {free_percent:.1f}% free'
            
            if free_percent < 20:
                status_level = 'warning'
                message = f'Low disk space: {free_percent:.1f}% free'
            elif free_percent < 10:
                status_level = 'unhealthy'
                message = f'Critical disk space: {free_percent:.1f}% free'
            
            return {
                'status': status_level,
                'message': message,
                'free_percent': round(free_percent, 1),
                'free_gb': round(disk_usage.free / (1024**3), 2),
                'total_gb': round(disk_usage.total / (1024**3), 2),
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Disk space check failed: {str(e)}',
                'timestamp': time.time()
            }
    
    def _check_memory(self):
        """Check memory usage"""
        try:
            # Simple memory check using /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = 0
            mem_available = 0
            
            for line in meminfo.split('\n'):
                if line.startswith('MemTotal:'):
                    mem_total = int(line.split()[1]) * 1024  # Convert KB to bytes
                elif line.startswith('MemAvailable:'):
                    mem_available = int(line.split()[1]) * 1024  # Convert KB to bytes
            
            if mem_total > 0:
                used_percent = ((mem_total - mem_available) / mem_total) * 100
                
                status_level = 'healthy'
                message = f'Memory usage: {used_percent:.1f}%'
                
                if used_percent > 80:
                    status_level = 'warning'
                    message = f'High memory usage: {used_percent:.1f}%'
                elif used_percent > 95:
                    status_level = 'unhealthy'
                    message = f'Critical memory usage: {used_percent:.1f}%'
                
                return {
                    'status': status_level,
                    'message': message,
                    'used_percent': round(used_percent, 1),
                    'available_gb': round(mem_available / (1024**3), 2),
                    'total_gb': round(mem_total / (1024**3), 2),
                    'timestamp': time.time()
                }
            else:
                return {
                    'status': 'warning',
                    'message': 'Could not determine memory usage',
                    'timestamp': time.time()
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Memory check failed: {str(e)}',
                'timestamp': time.time()
            }
    
    def _check_cpu(self):
        """Check CPU usage"""
        try:
            # Simple CPU check using load average
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            # Get CPU count from /proc/cpuinfo
            cpu_count = 1
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpu_count = len([line for line in f if line.startswith('processor')])
            except:
                cpu_count = 1
            
            # Use 1-minute load average as CPU usage indicator
            cpu_load = load_avg[0] if load_avg else 0
            cpu_percent = (cpu_load / cpu_count) * 100 if cpu_count > 0 else 0
            
            status_level = 'healthy'
            message = f'CPU load: {cpu_load:.2f} ({cpu_percent:.1f}%)'
            
            if cpu_percent > 80:
                status_level = 'warning'
                message = f'High CPU load: {cpu_load:.2f} ({cpu_percent:.1f}%)'
            elif cpu_percent > 150:
                status_level = 'unhealthy'
                message = f'Critical CPU load: {cpu_load:.2f} ({cpu_percent:.1f}%)'
            
            return {
                'status': status_level,
                'message': message,
                'cpu_load': round(cpu_load, 2),
                'cpu_count': cpu_count,
                'load_avg': load_avg,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'CPU check failed: {str(e)}',
                'timestamp': time.time()
            }
    
    def _check_external_apis(self):
        """Check external API connectivity"""
        try:
            import requests
            
            # Test GBIF API
            start_time = time.time()
            response = requests.get('https://api.gbif.org/v1/species/search?q=Puma', timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                status_level = 'healthy'
                message = 'External APIs are accessible'
                
                if response_time > 5000:  # 5 seconds
                    status_level = 'warning'
                    message = f'External API response time is high: {response_time:.2f}ms'
            else:
                status_level = 'warning'
                message = f'External API returned status {response.status_code}'
            
            return {
                'status': status_level,
                'message': message,
                'gbif_response_time_ms': round(response_time, 2),
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'External API check failed: {str(e)}',
                'timestamp': time.time()
            }


# Global health check service instance
health_service = HealthCheckService()


@api_view(['GET'])
def health_check(request):
    """
    Comprehensive health check endpoint
    
    Returns detailed health information about all system components
    """
    results = health_service.run_all_checks()
    
    # Set appropriate HTTP status code
    if results['status'] == 'healthy':
        http_status = status.HTTP_200_OK
    elif results['status'] == 'warning':
        http_status = status.HTTP_200_OK  # Still operational
    else:
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JsonResponse(results, status=http_status)


@api_view(['GET'])
def health_check_simple(request):
    """
    Simple health check endpoint for load balancers
    
    Returns basic OK/ERROR status
    """
    try:
        # Quick database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return JsonResponse({
            'status': 'OK',
            'timestamp': time.time()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Simple health check failed: {str(e)}")
        return JsonResponse({
            'status': 'ERROR',
            'message': str(e),
            'timestamp': time.time()
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def readiness_check(request):
    """
    Readiness check for Kubernetes/container orchestration
    
    Checks if the application is ready to serve requests
    """
    try:
        # Check critical dependencies
        checks = {
            'database': health_service._check_database(),
        }
        
        all_healthy = all(check['status'] == 'healthy' for check in checks.values())
        
        if all_healthy:
            return JsonResponse({
                'status': 'ready',
                'checks': checks,
                'timestamp': time.time()
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'status': 'not_ready',
                'checks': checks,
                'timestamp': time.time()
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def liveness_check(request):
    """
    Liveness check for Kubernetes/container orchestration
    
    Checks if the application is alive and should not be restarted
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': time.time()
    }, status=status.HTTP_200_OK)
