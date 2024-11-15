from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# views.py
from .forms import RedactarCorreoForm
from .models import Correo, User
from django.contrib.auth import get_user_model
from .forms import RedactarCorreoForm  # Vamos a crear este formulario
from django.shortcuts import get_object_or_404

@login_required
def filtrar_por_dominio(request):
    # Obtener todos los dominios únicos de los usuarios en el sistema
    usuarios = User.objects.values_list('username', flat=True)
    dominios = set(username.split('@')[-1] for username in usuarios if '@' in username)

    # Obtener el dominio seleccionado en el combo box
    dominio_seleccionado = request.GET.get('dominio')

    # Obtener el usuario actual para mostrar solo los correos recibidos
    usuario_actual = request.user

    # Filtrar los correos recibidos por el usuario actual y el dominio seleccionado
    if dominio_seleccionado:
        correos = Correo.objects.filter(
            destinatario=usuario_actual,
            remitente__username__endswith=f"@{dominio_seleccionado}",
            eliminado_por_destinatario=False
        ).order_by('-fecha_envio')
    else:
        correos = [] # O puedes cargar todos los correos si quieres

    return render(request, 'emails/filtrar_por_dominio.html', {
        'dominios': dominios,
        'correos': correos,
        'dominio_seleccionado': dominio_seleccionado,
    })


@login_required
def marcar_como_no_leido(request, correo_id):
    # Obtener el correo que se desea actualizar
    correo = get_object_or_404(Correo, id=correo_id)
    
    # Cambiar el estado de "leido" a False
    correo.leido = False
    correo.save()
    
    # Redirigir de nuevo a la bandeja de entrada (o cualquier otra vista)
    return redirect('inbox')
@login_required
def correos_no_leidos(request):
    # Filtrar solo los correos que han llegado al usuario actual y que no han sido leídos
    correos_no_leidos = Correo.objects.filter(destinatario=request.user, leido=False,eliminado_por_destinatario=False)
    
    return render(request, 'emails/correos_no_leidos.html', {
        'correos_no_leidos': correos_no_leidos
    })

@login_required
def correos_alta_prioridad_view(request):
    # Filtrar los correos de alta prioridad
    correos_alta_prioridad = Correo.objects.filter(destinatario=request.user, prioridad__nivel="Alta", eliminado_por_destinatario=False).order_by('-fecha_envio')
    return render(request, 'emails/correos_alta_prioridad.html', {
        'correos_alta_prioridad': correos_alta_prioridad,
    })

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
    correos_eliminados = Correo.objects.filter(destinatario=request.user, eliminado_por_destinatario=True).order_by('-fecha_envio')
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
    correos_enviados = Correo.objects.filter(remitente=request.user).order_by('-fecha_envio')
    return render(request, 'emails/correos_enviados.html', {'correos_enviados': correos_enviados})

# Vista para ver un correo
@login_required
def ver_correo(request, correo_id):
    correo = Correo.objects.get(id=correo_id)
    if correo.destinatario == request.user and not correo.leido:
        correo.leido = True
        correo.save()
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

@login_required  
def inbox_view(request):
    # Vista de bandeja de entrada
    correos_recibidos = Correo.objects.filter(destinatario=request.user,eliminado_por_destinatario=False).order_by('-fecha_envio')
    return render(request, 'emails/inbox.html', {'correos_recibidos': correos_recibidos})
