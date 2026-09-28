from django.db import models
from zonas.models import Zona

class Propiedad(models.Model):
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    precio = models.CharField(max_length=50)  # Ejemplo: '4.500 UF'
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    descripcion = models.TextField()
    
    # Agregamos la relación (ForeignKey) para cumplir con la rúbrica
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True, related_name='propiedades')

    def __str__(self):
        return self.titulo
