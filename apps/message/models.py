from django.db import models
from users.models import Usuario


# Create your models here.

class Conversacion(models.Model):
    usuario_emisor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='conversaciones_enviadas'
    )
    usuario_receptor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='conversaciones_recibidas'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario_emisor} → {self.usuario_receptor}"

    class Meta:
        db_table = 'Conversacion'


class Mensaje(models.Model):
    conversacion = models.ForeignKey(
        Conversacion, on_delete=models.CASCADE,
        related_name='mensajes'
    )
    usuario_emisor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #Se utilizara para las imagenes(local pero debera cambiarse a la nube)
   # imagen = models.ImageField(upload_to='mensajes/', null=True, blank=True) 

    def __str__(self):
        return f"{self.usuario_emisor}: {self.contenido[:40]}"

    class Meta:
        db_table = 'Mensaje'
        ordering = ['created_at']