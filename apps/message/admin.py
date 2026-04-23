from django.contrib import admin
from .models import Conversacion, Mensaje

# Register your models here.
class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 1

@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario_emisor', 'usuario_receptor', 'created_at']
    inlines = [MensajeInline]

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversacion', 'usuario_emisor', 'contenido', 'created_at']