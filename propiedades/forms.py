from django import forms

class PropiedadForm(forms.Form):
    titulo = forms.CharField(label="Título de la propiedad", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.CharField(label="Tipo (Casa, Departamento, etc.)", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    precio = forms.CharField(label="Precio", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    habitaciones = forms.IntegerField(label="Habitaciones", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    banos = forms.IntegerField(label="Baños", widget=forms.NumberInput(attrs={'class': 'form-control'}))