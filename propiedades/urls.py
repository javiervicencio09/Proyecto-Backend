from django.urls import path
from . import views

app_name = 'propiedades'

urlpatterns = [
    path('', views.lista_propiedades, name='lista'),
    path('<int:id_propiedad>/', views.detalle_propiedad, name='detalle'),
    path('agregar/', views.agregar_propiedad, name='agregar'),
    path('editar/<int:id_propiedad>/', views.editar_propiedad, name='editar'),
    path('eliminar/<int:id_propiedad>/', views.eliminar_propiedad, name='eliminar'),
]
