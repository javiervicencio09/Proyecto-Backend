import json
import os
from django.shortcuts import redirect, render
from django.conf import settings
from .forms import PropiedadForm

def lista_propiedades(request):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'propiedades.json')
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_propiedades = json.load(archivo)
        
    contexto = {
        'propiedades': datos_propiedades
    }
    return render(request, 'propiedades/lista.html', contexto)

def detalle_propiedad(request, id_propiedad):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'propiedades.json')
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos_propiedades = json.load(archivo)
        
    propiedad_encontrada = None
    for propiedad in datos_propiedades:
        if propiedad['id'] == id_propiedad:
            propiedad_encontrada = propiedad
            break
            
    contexto = {
        'propiedad': propiedad_encontrada
    }
    return render(request, 'propiedades/detalle.html', contexto)

def home(request):
    return render(request, 'home.html')

def agregar_propiedad(request):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'propiedades.json')

    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                propiedades = json.load(f)
            nuevo_id = propiedades[-1]['id'] + 1 if propiedades else 1
            nueva_prop = {
                'id': nuevo_id,
                'titulo': form.cleaned_data['titulo'],
                'tipo': form.cleaned_data['tipo'],
                'precio': form.cleaned_data['precio'],
                'descripcion': form.cleaned_data['descripcion'],
                'habitaciones': form.cleaned_data['habitaciones'],
                'banos': form.cleaned_data['banos'],
            }
            propiedades.append(nueva_prop)
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(propiedades, f, ensure_ascii=False, indent=4)
            return redirect('propiedades:lista')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/agregar.html', {'form': form})