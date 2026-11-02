from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Zona
from .forms import ZonaForm
from usuarios.decoradores import supervisor_requerido, admin_requerido

def lista_zonas(request):
    query = request.GET.get('q', '').strip()
    demanda = request.GET.get('demanda', '').strip()

    zonas = Zona.objects.annotate(total_propiedades=Count('propiedades')).all()

    if query:
        zonas = zonas.filter(
            Q(nombre__icontains=query) | Q(destacado__icontains=query)
        )

    if demanda:
        zonas = zonas.filter(nivel_demanda__iexact=demanda)

    contexto = {
        'zonas': zonas,
        'q': query,
        'demanda_seleccionada': demanda,
        'total_resultados': zonas.count(),
    }
    return render(request, 'zonas/lista_zonas.html', contexto)

@supervisor_requerido
def crear_zona(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            zona = form.save()
            messages.success(request, f"¡Zona '{zona.nombre}' creada con éxito!")
            return redirect('zonas:lista')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = ZonaForm()

    return render(request, 'zonas/crear_zona.html', {'form': form})

@supervisor_requerido
def editar_zona(request, id_zona):
    zona = get_object_or_404(Zona, id=id_zona)

    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Zona '{zona.nombre}' actualizada con éxito!")
            return redirect('zonas:lista')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = ZonaForm(instance=zona)

    return render(request, 'zonas/editar_zona.html', {'form': form, 'zona': zona})

@admin_requerido
def eliminar_zona(request, id_zona):
    zona = get_object_or_404(Zona.objects.annotate(total_propiedades=Count('propiedades')), id=id_zona)

    if request.method == 'POST':
        nombre = zona.nombre
        zona.delete()
        messages.success(request, f"La zona '{nombre}' ha sido eliminada del sistema.")
        return redirect('zonas:lista')

    return render(request, 'zonas/eliminar_zona.html', {'zona': zona})
