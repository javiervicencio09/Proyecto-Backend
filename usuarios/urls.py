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

    # Flujo de Recuperación de Contraseña por Correo (Tokens)
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
