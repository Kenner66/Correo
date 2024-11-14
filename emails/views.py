from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# views.py
from .forms import RedactarCorreoForm
from .models import Correo, User
from django.contrib.auth import get_user_model
from .forms import RedactarCorreoForm  # Vamos a crear este formulario
from django.shortcuts import get_object_or_404

@login_required
def restaurar_correo(request, correo_id):
    # Obtener el correo o devolver un 404 si no existe
    correo = get_object_or_404(Correo, id=correo_id, destinatario=request.user, eliminado_por_destinatario=True)

    # Restaurar el correo para el destinatario
    correo.eliminado_por_destinatario = False
    correo.save()

    # Redirigir de nuevo a la lista de correos eliminados
    return redirect('correos_eliminados')
@login_required
def correos_eliminados_view(request):
    # Filtrar correos eliminados por el usuario actual
    correos_eliminados = Correo.objects.filter(destinatario=request.user, eliminado_por_destinatario=True)
    return render(request, 'emails/correos_eliminados.html', {'correos_eliminados': correos_eliminados})

@login_required
def eliminar_correo_recibido(request, correo_id):
    # Obtener el correo o devolver un 404 si no existe
    correo = get_object_or_404(Correo, id=correo_id, destinatario=request.user)

    # Marcar el correo como eliminado solo para el destinatario
    correo.eliminado_por_destinatario = True
    correo.save()

    # Redirigir de nuevo a la bandeja de entrada
    return redirect('inbox')


@login_required
def correos_enviados_view(request):
    # Filtrar correos enviados por el usuario actual
    correos_enviados = Correo.objects.filter(remitente=request.user)
    return render(request, 'emails/correos_enviados.html', {'correos_enviados': correos_enviados})

# Vista para ver un correo
@login_required
def ver_correo(request, correo_id):
    correo = Correo.objects.get(id=correo_id)
    return render(request, 'emails/ver_correo.html', {'correo': correo})

@login_required
def redactar_correo(request):
    if request.method == "POST":
        form = RedactarCorreoForm(request.POST,usuario_actual=request.user)
        if form.is_valid():
            correo = form.save(commit=False)
            correo.remitente = request.user  # Asignar el remitente al usuario logueado
            correo.save()  # Guardar el correo
            return redirect('inbox')  # Redirigir a la bandeja de entrada
    else:
        form = RedactarCorreoForm(usuario_actual=request.user)
    
    return render(request, 'emails/redactar_correo.html', {'form': form})



@login_required  # Asegura que solo usuarios autenticados puedan acceder
def inbox_view(request):
    # Vista de bandeja de entrada
    correos_recibidos = Correo.objects.filter(destinatario=request.user,eliminado_por_destinatario=False)
    return render(request, 'emails/inbox.html', {'correos_recibidos': correos_recibidos})
