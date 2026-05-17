from django.urls import path
from . import views

urlpatterns = [
    path('mensajes/', views.bandeja, name='bandeja'),
    path('mensajes/<int:conversacion_id>/', views.conversacion, name='conversacion'),
     path('mensajes/iniciar/<int:receptor_id>/', views.iniciar_conversacion, name='iniciar_conversacion'),
    # Nueva vista para crear conversación desde draft:
    path('mensajes/nueva/', views.crear_conversacion, name='crear_conversacion'),
]