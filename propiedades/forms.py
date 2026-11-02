from datetime import date
from django import forms
from .models import Propiedad, ReservaVisita

TIPOS_PROPIEDAD = [
    ('', 'Seleccione un tipo...'),
    ('Casa', 'Casa'),
    ('Departamento', 'Departamento'),
    ('Terreno / Parcela', 'Terreno / Parcela'),
    ('Oficina / Comercial', 'Oficina / Comercial'),
]

class PropiedadForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=TIPOS_PROPIEDAD,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Propiedad
        fields = ['titulo', 'tipo', 'precio', 'descripcion', 'habitaciones', 'banos', 'zona']
        labels = {
            'titulo': 'Título de la Propiedad',
            'tipo': 'Tipo de Inmueble',
            'precio': 'Precio (ej. 3.200 UF o $85.000.000)',
            'descripcion': 'Descripción detallada',
            'habitaciones': 'Número de Habitaciones',
            'banos': 'Número de Baños',
            'zona': 'Zona / Comuna',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Moderna Casa en La Serena'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 4.500 UF'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detalles de la propiedad, cercanías, servicios...'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'banos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'zona': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_habitaciones(self):
        habs = self.cleaned_data.get('habitaciones')
        if habs is not None and habs < 0:
            raise forms.ValidationError("El número de habitaciones no puede ser negativo.")
        return habs

    def clean_banos(self):
        banos = self.cleaned_data.get('banos')
        if banos is not None and banos < 0:
            raise forms.ValidationError("El número de baños no puede ser negativo.")
        return banos

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo


class ReservaVisitaForm(forms.ModelForm):
    class Meta:
        model = ReservaVisita
        fields = ['propiedad', 'cliente_nombre', 'cliente_email', 'cliente_telefono', 'fecha_visita', 'hora_visita', 'comentarios']
        labels = {
            'propiedad': 'Propiedad a Visitar',
            'cliente_nombre': 'Nombre Completo del Cliente',
            'cliente_email': 'Correo Electrónico',
            'cliente_telefono': 'Teléfono de Contacto',
            'fecha_visita': 'Fecha de la Visita',
            'hora_visita': 'Hora de la Visita',
            'comentarios': 'Notas o Requerimientos Especiales',
        }
        widgets = {
            'propiedad': forms.Select(attrs={'class': 'form-select'}),
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez González'}),
            'cliente_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@correo.cl'}),
            'cliente_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'fecha_visita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_visita': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Indica consultas previas o rango horario preferido...'}),
        }

    def clean_fecha_visita(self):
        fecha = self.cleaned_data.get('fecha_visita')
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha de visita no puede ser anterior a hoy.")
        return fecha

    def clean_cliente_telefono(self):
        telefono = self.cleaned_data.get('cliente_telefono', '').strip()
        if len(telefono) < 8:
            raise forms.ValidationError("Ingresa un número telefónico válido (al menos 8 caracteres).")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        propiedad = cleaned_data.get('propiedad')
        fecha = cleaned_data.get('fecha_visita')
        hora = cleaned_data.get('hora_visita')

        if propiedad and fecha and hora:
            # Validar que no exista ya una visita Confirmada para la misma propiedad y hora
            existe_solape = ReservaVisita.objects.filter(
                propiedad=propiedad,
                fecha_visita=fecha,
                hora_visita=hora,
                estado='Confirmada'
            ).exclude(pk=self.instance.pk if self.instance else None).exists()

            if existe_solape:
                raise forms.ValidationError(
                    f"Ya existe una visita confirmada para '{propiedad.titulo}' en la fecha {fecha} a las {hora}. Por favor elige otro horario."
                )
        return cleaned_data


class CambiarEstadoVisitaForm(forms.ModelForm):
    class Meta:
        model = ReservaVisita
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
