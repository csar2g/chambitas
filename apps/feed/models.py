from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Publicacion(models.Model):
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.created_at)

class ImagenPublicacion(models.Model):
    publicacion = models.ForeignKey(
        Publicacion, 
        on_delete=models.CASCADE, 
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='publicaciones/')

    def __str__(self):
        return f"Imagen de {self.publicacion.id}"

class Reaccion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='reacciones')

    def __str__(self):
        return f"{self.user} -> {self.publicacion}"

class Comentario(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    contenido = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return self.contenido
