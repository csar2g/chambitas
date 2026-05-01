from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
]
