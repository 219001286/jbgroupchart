from django import http
from django.contrib import admin
from django.urls import path,include
from base import api
from django.conf import settings
from django.conf.urls.static import static

# practice of the httpresponse interact with views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)