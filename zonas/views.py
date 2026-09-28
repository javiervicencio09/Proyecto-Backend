import json
import os
from django.shortcuts import render
from django.conf import settings

def lista_zonas(request):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'zonas.json')
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_zonas = json.load(archivo)

    contexto = {
        'zonas': datos_zonas
    }
    return render(request, 'zonas/lista_zonas.html', contexto)