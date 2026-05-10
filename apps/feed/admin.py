from django.contrib import admin
from .models import Publicacion, Reaccion, Comentario

# Register your models here.

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display=('descripcion', 'user', 'created_at', 'updated_at')


@admin.register(Reaccion)
class ReaccionAdmin(admin.ModelAdmin):
    list_display=('created_at', 'user', 'publicacion')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display=('created_at', 'contenido', 'user', 'publicacion')
