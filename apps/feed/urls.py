from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('search-users/', views.search_users, name='search_users'),
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('like/<int:publicacion_id>/', views.toggle_like, name='toggle_like')
]
