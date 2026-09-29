# pyrefly: ignore [missing-import]
from django.db import models

class Zona(models.Model):
    nombre = models.CharField(max_length=150)
    destacado = models.CharField(max_length=200)
    nivel_demanda = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
