from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from propiedades.models import Propiedad
from zonas.models import Zona
from .forms import CustomLoginForm
from .decoradores import (
    obtener_rol_usuario,
    admin_requerido,
    supervisor_requerido,
    administrativo_requerido
)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            rol = obtener_rol_usuario(user)
            messages.success(request, f"¡Bienvenido, {user.first_name or user.username}! Has ingresado con perfil {rol}.")
            return redirect('usuarios:dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Por favor, verifica tus credenciales.")
    else:
        form = CustomLoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('usuarios:login')

@login_required
def dashboard_redirect(request):
    rol = obtener_rol_usuario(request.user)
    if rol == 'Administrador':
        return redirect('usuarios:dashboard_admin')
    elif rol == 'Supervisor':
        return redirect('usuarios:dashboard_supervisor')
    elif rol == 'Administrativo':
        return redirect('usuarios:dashboard_administrativo')
    else:
        messages.warning(request, "Tu cuenta no tiene un rol asignado. Contacta al administrador.")
        return redirect('home')

@admin_requerido
def dashboard_admin(request):
    contexto = {
        'total_propiedades': Propiedad.objects.count(),
        'total_zonas': Zona.objects.count(),
        'total_usuarios': User.objects.count(),
        'ultimas_propiedades': Propiedad.objects.select_related('zona').order_by('-id')[:5],
        'usuarios': User.objects.prefetch_related('groups').all()[:10],
    }
    return render(request, 'usuarios/dashboard_admin.html', contexto)

@supervisor_requerido
def dashboard_supervisor(request):
    contexto = {
        'total_propiedades': Propiedad.objects.count(),
        'total_zonas': Zona.objects.count(),
        'ultimas_propiedades': Propiedad.objects.select_related('zona').order_by('-id')[:5],
        'zonas': Zona.objects.all()[:5],
    }
    return render(request, 'usuarios/dashboard_supervisor.html', contexto)

@administrativo_requerido
def dashboard_administrativo(request):
    contexto = {
        'total_propiedades': Propiedad.objects.count(),
        'ultimas_propiedades': Propiedad.objects.select_related('zona').order_by('-id')[:8],
    }
    return render(request, 'usuarios/dashboard_administrativo.html', contexto)
