from django import forms
from .models import Propiedad

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
