from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Persona, Mascota, Adopcion, ONG
from django.contrib.auth.forms import AuthenticationForm


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ONGForm(forms.ModelForm):
    class Meta:
        model = ONG
        fields = ['nombre', 'pais', 'telefono', 'correo', 'representante', 'sitio_web', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'representante': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }



class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ong': forms.Select(attrs={'class': 'form-control'}),
        }


class AdopcionForm(forms.ModelForm):
    class Meta:
        model = Adopcion
        fields = '__all__'
        widgets = {
            'fecha_adopcion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_fecha_adopcion(self):
        fecha = self.cleaned_data.get('fecha_adopcion')
        if fecha and fecha > timezone.now().date():
            raise ValidationError("La fecha de adopción no puede ser en el futuro.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        mascota = cleaned.get('mascota')
        if mascota and mascota.adoptada:
            raise ValidationError("Esta mascota ya aparece como adoptada en el sistema.")
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
