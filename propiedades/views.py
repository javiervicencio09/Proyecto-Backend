from django.shortcuts import redirect, render, get_object_or_404
from .models import Propiedad
from .forms import PropiedadForm

def lista_propiedades(request):
    datos_propiedades = Propiedad.objects.all()
    contexto = {
        'propiedades': datos_propiedades
    }
    return render(request, 'propiedades/lista.html', contexto)

def detalle_propiedad(request, id_propiedad):
    propiedad_encontrada = get_object_or_404(Propiedad, id=id_propiedad)
    contexto = {
        'propiedad': propiedad_encontrada
    }
    return render(request, 'propiedades/detalle.html', contexto)

def home(request):
    return render(request, 'home.html')

def agregar_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('propiedades:lista')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/agregar.html', {'form': form})