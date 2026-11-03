from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación y Dashboards
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/supervisor/', views.dashboard_supervisor, name='dashboard_supervisor'),
    path('dashboard/administrativo/', views.dashboard_administrativo, name='dashboard_administrativo'),

    # Gestión de Usuarios y Roles (Exclusivo Administrador)
    path('gestion/', views.lista_usuarios, name='lista_usuarios'),
    path('gestion/crear/', views.crear_usuario, name='crear_usuario'),
    path('gestion/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),

    # Recuperación de Contraseña con Código de 5 Dígitos
    path('password_reset/', views.solicitar_recuperacion_view, name='password_reset'),
    path('password_reset/codigo/', views.verificar_codigo_view, name='password_reset_codigo'),
]
