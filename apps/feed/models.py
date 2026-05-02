from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Publicacion(models.Model):
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    img = models.CharField(max_length=350, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.created_at)

class Reaccion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.publicacion

class Comentario(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    contenido = models.CharField(max_length=400)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.contenido
