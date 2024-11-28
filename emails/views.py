from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# views.py
from .forms import RedactarCorreoForm
from .models import Correo, User
from django.contrib.auth import get_user_model
from .forms import RedactarCorreoForm  # Vamos a crear este formulario
from django.shortcuts import get_object_or_404
from .utils import clasificar_por_asunto 
from .utils import CATEGORIAS_POR_PALABRAS
from django.core.paginator import Paginator
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from .models import Correo
from django.contrib.auth.decorators import login_required
from django.db import models
import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI


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
    # Clasificar los correos en un diccionario
    clasificados = {}
    for correo in correos_recibidos:
        categoria = clasificar_por_asunto(correo.asunto)
        if categoria not in clasificados:
            clasificados[categoria] = []
        clasificados[categoria].append(correo)

    for categoria, correos in clasificados.items():
        paginator = Paginator(correos, 10)  # Paginación para cada categoría
        page_number = request.GET.get(f'page_{categoria}')  # Usamos un parámetro de página único por categoría
        page_obj = paginator.get_page(page_number)  # Obtener los correos de la página actual

        clasificados[categoria] = page_obj  # Reemplazamos la lista de correos por el objeto de paginación

    # Pasar los correos clasificados al template
    return render(request, 'emails/inbox.html', {
        'correos_clasificados': clasificados
    })

# Función para crear gráficos
def crear_grafico(data, tipo='bar', titulo='Gráfico', labels=None):
    fig, ax = plt.subplots()

    # Verifica si los datos son None o vacíos antes de generar el gráfico
    if data is None or len(data) == 0:
        ax.text(0.5, 0.5, 'Sin Datos', horizontalalignment='center', verticalalignment='center', fontsize=12)
    else:
        if tipo == 'bar':
            ax.bar(labels, data)
        elif tipo == 'pie':
            ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        elif tipo == 'line':
            ax.plot(labels, data)

    ax.set_title(titulo)

    # Guardar la imagen en un buffer
    buf = io.BytesIO()

    try:
        # Si los datos son válidos, guarda la imagen
        if data is not None and len(data) > 0:
            plt.savefig(buf, format='png')
            buf.seek(0)
            imagen = base64.b64encode(buf.getvalue()).decode('utf-8')
        else:
            # Si no hay datos, asignamos una cadena vacía para evitar el error
            imagen = ''
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        imagen = ''  # Evitar pasar None
    finally:
        plt.close(fig)

    return imagen

# Vista principal (dashboard)
@login_required
def dashboard_view(request):
    # 1. Correos recibidos por prioridad
    correos = Correo.objects.filter(destinatario=request.user, eliminado_por_destinatario=False)
    prioridades = correos.values('prioridad__nivel').annotate(count=models.Count('id'))
    # Filtrar las prioridades que tienen None
    prioridades = [p for p in prioridades if p['prioridad__nivel'] is not None]
    prioridades_dict = {p['prioridad__nivel']: p['count'] for p in prioridades}

    # 3. Correos por categorías (según el asunto)
    categorias = {categoria: 0 for categoria in CATEGORIAS_POR_PALABRAS.keys()}

    # Iteramos sobre los correos y los clasificamos
    for correo in correos:
        categoria = clasificar_por_asunto(correo.asunto)
    
        # Incrementamos el contador de la categoría correspondiente
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias["Otros"] += 1
            
    categorias_filtradas = {categoria: count for categoria, count in categorias.items() if count > 0}

    # Crear los gráficos
    grafico_prioridad = crear_grafico(list(prioridades_dict.values()), 'bar', 'Correos por Prioridad', list(prioridades_dict.keys()))
    grafico_categoria = crear_grafico(list(categorias_filtradas.values()), 'pie', 'Correos por Categoría', list(categorias_filtradas.keys()))

    # Renderizar los gráficos en el template
    return render(request, 'emails/dashboard.html', {
        'grafico_prioridad': grafico_prioridad,
        'grafico_categoria': grafico_categoria,
    })