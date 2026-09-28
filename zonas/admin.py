from django.contrib import admin
from .models import Zona

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nivel_demanda', 'destacado')
    search_fields = ('nombre',)
