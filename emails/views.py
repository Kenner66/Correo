from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# views.py
from .forms import RedactarCorreoForm
from .models import Correo, User
from django.contrib.auth import get_user_model
from .forms import RedactarCorreoForm  # Vamos a crear este formulario

# Vista para ver un correo
@login_required
def ver_correo(request, correo_id):
    correo = Correo.objects.get(id=correo_id)
    return render(request, 'emails/ver_correo.html', {'correo': correo})

@login_required
def redactar_correo(request):
    if request.method == "POST":
        form = RedactarCorreoForm(request.POST)
        if form.is_valid():
            correo = form.save(commit=False)
            correo.remitente = request.user  # Asignar el remitente al usuario logueado
            correo.save()  # Guardar el correo
            return redirect('inbox')  # Redirigir a la bandeja de entrada
    else:
        form = RedactarCorreoForm()
    
    return render(request, 'emails/redactar_correo.html', {'form': form})

@login_required  # Asegura que solo usuarios autenticados puedan acceder
def inbox_view(request):
    # Vista de bandeja de entrada
    correos_recibidos = Correo.objects.filter(destinatario=request.user)
    return render(request, 'emails/inbox.html', {'correos_recibidos': correos_recibidos})
