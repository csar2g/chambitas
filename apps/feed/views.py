from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Publicacion, Reaccion, Comentario

@login_required(login_url='landing')
def feed_view(request):
    publicaciones = Publicacion.objects.all().order_by('-created_at')
    return render(request, "feed.html", {
                    'publicaciones': publicaciones
    })




