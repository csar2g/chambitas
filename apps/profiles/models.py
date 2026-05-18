from django.db import models
from django.contrib.auth.models import User
import os


def save_profile_image(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"user_{instance.usuario.id}{ext}"
    return os.path.join("profile_images", filename)


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column="usuario_id",
        related_name="perfil",
    )
    descripcion = models.TextField(blank=True)
    aptitudes = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to=save_profile_image, blank=True, null=True)
    numero_tel = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    ubicacion = models.CharField(max_length=120, blank=True)

    class Meta:
        db_table = "Perfil"


class Link(models.Model):
    TIPO_PORTFOLIO = "portfolio"
    TIPO_LINKEDIN = "linkedin"
    TIPO_CHOICES = (
        (TIPO_PORTFOLIO, "Portfolio"),
        (TIPO_LINKEDIN, "LinkedIn"),
    )

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="links")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_PORTFOLIO)
    nombre = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = "Link"
        constraints = [
            models.UniqueConstraint(fields=["perfil", "tipo"], name="unique_link_por_tipo")
        ]


class Seguimiento(models.Model):
    seguidor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="siguiendo"
    )
    seguido = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seguidores"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Seguimiento"
        constraints = [
            models.UniqueConstraint(
                fields=["seguidor", "seguido"], name="unique_seguimiento"
            )
        ]

    def __str__(self):
        return f"{self.seguidor.username} → {self.seguido.username}"
