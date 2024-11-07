
# forms.py
from django import forms
from .models import Correo
from django.contrib.auth import get_user_model
class RedactarCorreoForm(forms.ModelForm):
    
    User = get_user_model()
    destinatario = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Todos los usuarios registrados
        empty_label="Selecciona un destinatario",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un destinatario'})
    )

    class Meta:
        model = Correo
        fields = ['destinatario', 'asunto', 'contenido']
        widgets = {
            'asunto': forms.TextInput(attrs={'placeholder': 'Asunto'}),
            'contenido': forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí'}),
        }