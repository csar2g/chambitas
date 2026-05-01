from django.urls import path
from . import views

urlpatterns = [
    path('mensajes/', views.bandeja, name='bandeja'),
    path('mensajes/<int:conversacion_id>/', views.conversacion, name='conversacion'),
]