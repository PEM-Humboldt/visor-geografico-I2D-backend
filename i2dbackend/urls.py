"""i2dbackend URL Configuration
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from applications.common.health import health_check, health_check_simple, readiness_check, liveness_check

schema_view = get_schema_view(
   openapi.Info(
      title="Visor I2D API",
      default_version='v1',
      description="Colombian Biodiversity Data API - Instituto Alexander von Humboldt",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@humboldt.org.co"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    path('', redirect_to_admin, name='home'),
    path('admin/', admin.site.urls),

    # Health Check Endpoints
    path('health/', health_check, name='health-check'),
    path('health/simple/', health_check_simple, name='health-check-simple'),
    path('health/ready/', readiness_check, name='readiness-check'),
    path('health/live/', liveness_check, name='liveness-check'),

    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # se incluyen las urls de las apps
    re_path('',include('applications.dpto.urls')),
    re_path('',include('applications.mupio.urls')),
    re_path('',include('applications.mupiopolitico.urls')),
    re_path('',include('applications.gbif.urls')),
    re_path('',include('applications.user.urls')),
    path('api/', include('applications.projects.urls')),

    # AJAX endpoints for admin interface
    path('ajax/admin/projects/', include('applications.projects.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
