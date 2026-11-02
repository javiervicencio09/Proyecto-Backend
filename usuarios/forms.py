from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)

ROLES_CHOICES = [
    ('Administrador', 'Administrador (Acceso total)'),
    ('Supervisor', 'Supervisor (Operacional y mantenedores)'),
    ('Administrativo', 'Administrativo (Consultas y registros)'),
]

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. admin_demo',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Correo Electrónico Registrado",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@ejemplo.cl',
            'autofocus': True
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UsuarioCreacionForm(forms.ModelForm):
    rol = forms.ChoiceField(
        choices=ROLES_CHOICES,
        label="Perfil / Rol de Acceso",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Nombre de Usuario (Login)',
            'email': 'Correo Electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. mrodriguez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mrodriguez@correo.cl'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. María'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Rodríguez'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')

        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Las contraseñas ingresadas no coinciden.")
        if p1 and len(p1) < 8:
            self.add_error('password', "La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if self.cleaned_data['rol'] == 'Administrador':
            user.is_staff = True
        if commit:
            user.save()
            rol_name = self.cleaned_data['rol']
            grupo, _ = Group.objects.get_or_create(name=rol_name)
            user.groups.set([grupo])
        return user


class UsuarioEdicionForm(forms.ModelForm):
    rol = forms.ChoiceField(
        choices=ROLES_CHOICES,
        label="Perfil / Rol de Acceso",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'is_active': 'Cuenta Activa (Habilitada para ingresar)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            grupo = self.instance.groups.first()
            if grupo:
                self.fields['rol'].initial = grupo.name

    def save(self, commit=True):
        user = super().save(commit=commit)
        rol_name = self.cleaned_data.get('rol')
        if rol_name:
            grupo, _ = Group.objects.get_or_create(name=rol_name)
            user.groups.set([grupo])
        return user
