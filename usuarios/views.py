import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from propiedades.models import Propiedad
from zonas.models import Zona
from .forms import (
    CustomLoginForm,
    SolicitarCodigoResetForm,
    VerificarCodigoPasswordForm,
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

# ========================================================
# RECUPERACIÓN DE CONTRASEÑA CON CÓDIGO DE 5 DÍGITOS (OTP)
# ========================================================

def solicitar_recuperacion_view(request):
    if request.method == 'POST':
        form = SolicitarCodigoResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            user = User.objects.filter(email__iexact=email).first()

            if user:
                # Generar código numérico de 5 dígitos
                codigo = f"{random.randint(10000, 99999)}"
                request.session['reset_code'] = codigo
                request.session['reset_user_id'] = user.id
                request.session['reset_email'] = user.email
                request.session['reset_expires'] = (timezone.now() + timedelta(minutes=15)).timestamp()

                # Enviar correo con el código
                try:
                    send_mail(
                        subject=f"Código de seguridad: {codigo} - Portal Inmobiliario Coquimbo",
                        message=f"""Hola {user.first_name or user.username},

Has solicitado restablecer tu contraseña en el Portal Inmobiliario Coquimbo.

Tu código de verificación de 5 dígitos es:
===========================
      {codigo}
===========================

Ingresa este código en tu pantalla para definir tu nueva contraseña.
Este código es válido durante 15 minutos.

Si tú no realizaste esta solicitud, puedes ignorar este mensaje; tu contraseña actual continuará siendo la misma.

Atentamente,
Equipo de Soporte - Portal Inmobiliario Coquimbo""",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        f"¡Código de 5 dígitos enviado a {user.email}! Ingrésalo a continuación."
                    )
                    return redirect('usuarios:password_reset_codigo')
                except Exception as e:
                    messages.error(request, f"No se pudo enviar el correo: {e}")
            else:
                messages.error(request, "No se encontró ninguna cuenta asociada a ese correo electrónico.")
    else:
        form = SolicitarCodigoResetForm()

    return render(request, 'usuarios/password_reset.html', {'form': form})

def verificar_codigo_view(request):
    # Validar que exista una solicitud previa en sesión
    if not request.session.get('reset_code') or not request.session.get('reset_user_id'):
        messages.warning(request, "Por favor solicita un código de recuperación primero.")
        return redirect('usuarios:password_reset')

    email_destino = request.session.get('reset_email', '')

    if request.method == 'POST':
        form = VerificarCodigoPasswordForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo'].strip()
            codigo_sesion = request.session.get('reset_code')
            expiracion = request.session.get('reset_expires', 0)

            # 1. Validar si expiró (15 minutos)
            if timezone.now().timestamp() > expiracion:
                messages.error(request, "El código ha expirado. Por favor solicita uno nuevo.")
                return redirect('usuarios:password_reset')

            # 2. Validar coincidencia de código
            if codigo_ingresado != codigo_sesion:
                form.add_error('codigo', "El código de 5 dígitos ingresado es incorrecto.")
            else:
                # Código válido -> Cambiar contraseña
                user = get_object_or_404(User, id=request.session['reset_user_id'])
                user.set_password(form.cleaned_data['new_password1'])
                user.save()

                # Limpiar sesión
                for key in ['reset_code', 'reset_user_id', 'reset_email', 'reset_expires']:
                    if key in request.session:
                        del request.session[key]

                messages.success(request, "¡Tu contraseña ha sido restablecida con éxito! Ya puedes iniciar sesión.")
                return redirect('usuarios:login')
    else:
        form = VerificarCodigoPasswordForm()

    return render(request, 'usuarios/password_reset_codigo.html', {
        'form': form,
        'email_destino': email_destino
    })
