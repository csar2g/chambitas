from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('search-users/', views.search_users, name='search_users'),
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:publicacion_id>/', views.toggle_like, name='toggle_like'),
    path('buscar/', views.buscar_view, name='buscar'),
    path('publicacion/<int:publicacion_id>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    path('publicacion/<int:publicacion_id>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/<int:publicacion_id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
]
