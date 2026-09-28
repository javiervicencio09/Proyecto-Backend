from django.contrib import admin
from django.urls import path, include
from propiedades.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('propiedades/', include('propiedades.urls')),
    path('zonas/', include('zonas.urls')),
    path('', home, name='home'),
]