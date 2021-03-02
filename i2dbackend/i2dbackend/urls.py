"""i2dbackend URL Configuration
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # se incluyen las urls de las apps
    re_path('',include('applications.mupio.urls')),
]
