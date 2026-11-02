from django.urls import path
from . import views

app_name = 'propiedades'

urlpatterns = [
    path('', views.lista_propiedades, name='lista'),
    path('<int:id_propiedad>/', views.detalle_propiedad, name='detalle'),
    path('agregar/', views.agregar_propiedad, name='agregar'),
    path('editar/<int:id_propiedad>/', views.editar_propiedad, name='editar'),
    path('eliminar/<int:id_propiedad>/', views.eliminar_propiedad, name='eliminar'),

    # Rutas de Transacción Operacional: Visitas / Reservas
    path('visitas/', views.lista_visitas, name='lista_visitas'),
    path('visitas/agendar/', views.crear_visita, name='crear_visita'),
    path('visitas/agendar/<int:id_propiedad>/', views.crear_visita, name='agendar_visita_propiedad'),
    path('visitas/<int:id_visita>/estado/', views.cambiar_estado_visita, name='cambiar_estado_visita'),
]
