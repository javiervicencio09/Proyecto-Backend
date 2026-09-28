from django.urls import path
from . import views

app_name = 'zonas'

urlpatterns = [
    path('', views.lista_zonas, name='lista'),
]