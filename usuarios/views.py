from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.db.models import Q

from propiedades.models import Propiedad
from zonas.models import Zona
from .forms import (
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    UsuarioCreacionForm,
    UsuarioEdicionForm
)
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

# ==========================================
# GESTIÓN DE USUARIOS Y ROLES (SOLO ADMIN)
# ==========================================

@admin_requerido
def lista_usuarios(request):
    query = request.GET.get('q', '').strip()
    usuarios = User.objects.prefetch_related('groups').order_by('username')

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, 'usuarios/usuarios_lista.html', {
        'usuarios': usuarios,
        'q': query,
        'total_usuarios': usuarios.count(),
    })

@admin_requerido
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreacionForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            messages.success(
                request,
                f"Usuario '{nuevo_usuario.username}' creado con éxito con el perfil '{form.cleaned_data['rol']}'."
            )
            return redirect('usuarios:lista_usuarios')
        else:
            messages.error(request, "Por favor corrige los errores indicados en el formulario.")
    else:
        form = UsuarioCreacionForm()

    return render(request, 'usuarios/usuarios_crear.html', {'form': form})

@admin_requerido
def editar_usuario(request, id_usuario):
    usuario_obj = get_object_or_404(User.objects.prefetch_related('groups'), id=id_usuario)

    if request.method == 'POST':
        form = UsuarioEdicionForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            if usuario_obj == request.user and not form.cleaned_data.get('is_active'):
                messages.error(request, "No puedes desactivar tu propia cuenta de administrador.")
                return redirect('usuarios:lista_usuarios')

            form.save()
            messages.success(request, f"Datos y rol del usuario '{usuario_obj.username}' actualizados.")
            return redirect('usuarios:lista_usuarios')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UsuarioEdicionForm(instance=usuario_obj)

    return render(request, 'usuarios/usuarios_editar.html', {
        'form': form,
        'usuario_obj': usuario_obj
    })

# ==========================================
# RECUPERACIÓN DE CONTRASEÑA (EMAIL + TOKEN)
# ==========================================

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'usuarios/password_reset.html'
    email_template_name = 'usuarios/password_reset_email.html'
    subject_template_name = 'usuarios/password_reset_subject.txt'
    success_url = reverse_lazy('usuarios:password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'usuarios/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'usuarios/password_reset_confirm.html'
    success_url = reverse_lazy('usuarios:password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'usuarios/password_reset_complete.html'
