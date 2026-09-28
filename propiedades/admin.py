from django.contrib import admin
from .models import Propiedad

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'tipo', 'precio', 'zona')
    list_filter = ('tipo', 'zona')
    search_fields = ('titulo', 'descripcion')
