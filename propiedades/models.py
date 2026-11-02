from django.db import models
from django.contrib.auth.models import User
from zonas.models import Zona

class Propiedad(models.Model):
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    precio = models.CharField(max_length=50)  # Ejemplo: '4.500 UF'
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    descripcion = models.TextField()
    
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True, related_name='propiedades')

    def __str__(self):
        return self.titulo

class ReservaVisita(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada'),
    ]

    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='visitas')
    cliente_nombre = models.CharField(max_length=150, verbose_name="Nombre del Cliente")
    cliente_email = models.EmailField(verbose_name="Correo Electrónico")
    cliente_telefono = models.CharField(max_length=30, verbose_name="Teléfono")
    fecha_visita = models.DateField(verbose_name="Fecha de Visita")
    hora_visita = models.TimeField(verbose_name="Hora de Visita")
    comentarios = models.TextField(blank=True, verbose_name="Comentarios adicionales")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_visita', '-hora_visita']
        verbose_name = "Reserva de Visita"
        verbose_name_plural = "Reservas de Visitas"

    def __str__(self):
        return f"Visita #{self.id} - {self.propiedad.titulo} ({self.cliente_nombre})"
