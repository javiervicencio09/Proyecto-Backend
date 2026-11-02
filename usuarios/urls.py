from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/supervisor/', views.dashboard_supervisor, name='dashboard_supervisor'),
    path('dashboard/administrativo/', views.dashboard_administrativo, name='dashboard_administrativo'),
]

