from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def obtener_rol_usuario(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser or user.groups.filter(name='Administrador').exists():
        return 'Administrador'
    if user.groups.filter(name='Supervisor').exists():
        return 'Supervisor'
    if user.groups.filter(name='Administrativo').exists():
        return 'Administrativo'
    return 'Sin Rol'

def rol_requerido(roles_permitidos):
    """
    Decorador que verifica si el usuario autenticado tiene uno de los roles indicados.
    Los roles permitidos pueden ser: 'Administrador', 'Supervisor', 'Administrativo'.
    Si el usuario es superusuario, siempre tiene acceso.
    """
    def decorador(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            rol = obtener_rol_usuario(request.user)
            if rol in roles_permitidos:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                f"Acceso denegado: tu perfil ({rol}) no tiene permisos para acceder a esta sección."
            )
            return redirect('usuarios:dashboard')
        return wrapper
    return decorador

def admin_requerido(view_func):
    return rol_requerido(['Administrador'])(view_func)

def supervisor_requerido(view_func):
    return rol_requerido(['Administrador', 'Supervisor'])(view_func)

def administrativo_requerido(view_func):
    return rol_requerido(['Administrador', 'Supervisor', 'Administrativo'])(view_func)

