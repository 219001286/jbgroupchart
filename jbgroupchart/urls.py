from django import http
from django.contrib import admin
from django.urls import path,include


# practice of the httpresponse interact with views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]
