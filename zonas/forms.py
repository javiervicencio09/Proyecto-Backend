from django import forms
from .models import Zona

NIVELES_DEMANDA = [
    ('', 'Seleccione nivel de demanda...'),
    ('Alta', 'Alta'),
    ('Media', 'Media'),
    ('Baja', 'Baja'),
]

class ZonaForm(forms.ModelForm):
    nivel_demanda = forms.ChoiceField(
        choices=NIVELES_DEMANDA,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Zona
        fields = ['nombre', 'destacado', 'nivel_demanda']
        labels = {
            'nombre': 'Nombre del Sector o Comuna',
            'destacado': 'Punto o Atractivo Destacado',
            'nivel_demanda': 'Nivel de Demanda Inmobiliaria',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. San Joaquín, La Serena'}),
            'destacado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Zona residencial de alta plusvalía y colegios cercanos'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre de la zona debe tener al menos 3 caracteres.")
        return nombre

