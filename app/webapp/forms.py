import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Nombre', max_length=64)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Apellido', max_length=64)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Correo', max_length=64)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=128)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}), max_length=128)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Ambas contraseñas deben ser iguales')

    def clean_email(self):
        username = self.cleaned_data['email']
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Ha ocurrido un error')

class ProductReservationForm(forms.Form):
    quantity = forms.IntegerField(
        label='Cantidad',
        min_value=1
        )
