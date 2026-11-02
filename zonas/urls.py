from django.urls import path
from . import views

app_name = 'zonas'

urlpatterns = [
    path('', views.lista_zonas, name='lista'),
    path('crear/', views.crear_zona, name='crear'),
    path('editar/<int:id_zona>/', views.editar_zona, name='editar'),
    path('eliminar/<int:id_zona>/', views.eliminar_zona, name='eliminar'),
]
