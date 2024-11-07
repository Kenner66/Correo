
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('redactar/', views.redactar_correo, name='redactar_correo'),
    path('ver_correo/<int:correo_id>/', views.ver_correo, name='ver_correo'),
]