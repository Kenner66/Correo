from django import forms
from .models import Correo
from django.contrib.auth import get_user_model

class RedactarCorreoForm(forms.ModelForm):
    User = get_user_model()

    destinatario = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Selecciona un destinatario",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un destinatario'})
    )

    archivos_adjuntos = forms.FileField(
        required=False,  # No obligatorio, manejar múltiples archivos en la vista
        label="Adjuntar archivos"
    )

    class Meta:
        model = Correo
        fields = ['prioridad', 'destinatario', 'asunto', 'contenido']
        widgets = {
            'prioridad': forms.Select(),
            'asunto': forms.TextInput(attrs={'placeholder': 'Asunto'}),
            'contenido': forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí'}),
        }

    def __init__(self, *args, usuario_actual=None, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario_actual:
            self.fields['destinatario'].queryset = self.User.objects.filter(
                is_superuser=False
            ).exclude(id=usuario_actual.id)
