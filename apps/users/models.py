from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="usuario_app",
        null=True,
        blank=True,
    )
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    estado = models.CharField(
        max_length=10,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')],
        default='activo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Usuario'
