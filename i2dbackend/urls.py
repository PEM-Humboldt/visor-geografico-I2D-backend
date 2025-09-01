"""i2dbackend URL Configuration
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # se incluyen las urls de las apps
    re_path('',include('applications.dpto.urls')),
    re_path('',include('applications.mupio.urls')),
    re_path('',include('applications.mupiopolitico.urls')),
    re_path('',include('applications.gbif.urls')),
    re_path('',include('applications.user.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
