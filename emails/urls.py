
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('eliminar-correo-recibido/<int:correo_id>/', views.eliminar_correo_recibido, name='eliminar_correo_recibido'),
    path('redactar/', views.redactar_correo, name='redactar_correo'),
    path('ver_correo/<int:correo_id>/', views.ver_correo, name='ver_correo'),
    path('correos-enviados/', views.correos_enviados_view, name='correos_enviados'),
    path('correos-eliminados/', views.correos_eliminados_view, name='correos_eliminados'),
    path('restaurar-correo/<int:correo_id>/', views.restaurar_correo, name='restaurar_correo'),
    path('correos-alta-prioridad/', views.correos_alta_prioridad_view, name='correos_alta_prioridad'),
    path('correos-no-leidos/', views.correos_no_leidos, name='correos_no_leidos'),
    path('marcar-como-no-leido/<int:correo_id>/', views.marcar_como_no_leido, name='marcar_como_no_leido'),
    path('filtrar-por-dominio/', views.filtrar_por_dominio, name='filtrar_por_dominio'),
]