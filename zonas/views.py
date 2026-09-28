from django.shortcuts import render
from .models import Zona

def lista_zonas(request):
    datos_zonas = Zona.objects.all()
    contexto = {
        'zonas': datos_zonas
    }
    return render(request, 'zonas/lista_zonas.html', contexto)