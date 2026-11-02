from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Propiedad
from .forms import PropiedadForm
from zonas.models import Zona
from usuarios.decoradores import supervisor_requerido, administrativo_requerido

def home(request):
    propiedades_destacadas = Propiedad.objects.select_related('zona').order_by('-id')[:3]
    zonas_destacadas = Zona.objects.all()[:4]
    return render(request, 'home.html', {
        'propiedades_destacadas': propiedades_destacadas,
        'zonas_destacadas': zonas_destacadas,
    })

def lista_propiedades(request):
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    zona_id = request.GET.get('zona', '').strip()

    propiedades = Propiedad.objects.select_related('zona').all()

    if query:
        propiedades = propiedades.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    if tipo:
        propiedades = propiedades.filter(tipo__iexact=tipo)

    if zona_id and zona_id.isdigit():
        propiedades = propiedades.filter(zona_id=int(zona_id))

    contexto = {
        'propiedades': propiedades,
        'zonas': Zona.objects.all(),
        'q': query,
        'tipo_seleccionado': tipo,
        'zona_seleccionada': int(zona_id) if (zona_id and zona_id.isdigit()) else '',
        'total_resultados': propiedades.count(),
    }
    return render(request, 'propiedades/lista.html', contexto)

def detalle_propiedad(request, id_propiedad):
    propiedad = get_object_or_404(Propiedad.objects.select_related('zona'), id=id_propiedad)
    return render(request, 'propiedades/detalle.html', {'propiedad': propiedad})

@administrativo_requerido
def agregar_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            propiedad = form.save()
            messages.success(request, f"¡Propiedad '{propiedad.titulo}' creada con éxito!")
            return redirect('propiedades:lista')
        else:
            messages.error(request, "Por favor corrige los errores indicados en el formulario.")
    else:
        form = PropiedadForm()

    return render(request, 'propiedades/agregar.html', {
        'form': form,
        'titulo_accion': 'Registrar Nueva Propiedad'
    })

@supervisor_requerido
def editar_propiedad(request, id_propiedad):
    propiedad = get_object_or_404(Propiedad, id=id_propiedad)

    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Propiedad '{propiedad.titulo}' actualizada correctamente!")
            return redirect('propiedades:detalle', id_propiedad=propiedad.id)
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = PropiedadForm(instance=propiedad)

    return render(request, 'propiedades/editar.html', {
        'form': form,
        'propiedad': propiedad,
        'titulo_accion': 'Modificar Propiedad'
    })

@supervisor_requerido
def eliminar_propiedad(request, id_propiedad):
    propiedad = get_object_or_404(Propiedad, id=id_propiedad)

    if request.method == 'POST':
        titulo = propiedad.titulo
        propiedad.delete()
        messages.success(request, f"La propiedad '{titulo}' ha sido eliminada del catálogo.")
        return redirect('propiedades:lista')

    return render(request, 'propiedades/eliminar.html', {'propiedad': propiedad})
