from django.urls import path
from . import views

urlpatterns = [
    path('mensajes/<int:usuario_id>/', views.bandeja, name='bandeja'),
    path('mensajes/<int:usuario_id>/<int:conversacion_id>/', views.conversacion, name='conversacion'),
]