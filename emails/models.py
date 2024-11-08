
# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Correo(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enviados")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="correos_recibidos")  # Mantienes la relación ManyToMany
    asunto = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asunto


class Destinatario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="correos_destinatarios")  # Cambio en related_name
    correo = models.ForeignKey(Correo, on_delete=models.CASCADE, related_name="destinatarios_correo")  # Cambio en related_name

    def __str__(self):
        return f"{self.usuario} - {self.correo.asunto}"


class ArchivoAdjunto(models.Model):
    correo = models.ForeignKey(Correo, on_delete=models.CASCADE, related_name='archivos_adjuntos')
    nombre_archivo = models.CharField(max_length=255)
    ruta_archivo = models.FileField(upload_to='archivos/adjuntos/')

    def __str__(self):
        return self.nombre_archivo
    
    
class Carpeta(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carpetas')
    correos = models.ManyToManyField(Correo, blank=True, related_name='carpetas')

    def __str__(self):
        return f"{self.nombre} - {self.usuario}"
