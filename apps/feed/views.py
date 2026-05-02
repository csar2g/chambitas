from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Publicacion, Reaccion, Comentario
from profiles.models import Perfil

@login_required(login_url='landing')
def feed_view(request):
    publicaciones = Publicacion.objects.all().order_by('-created_at')
    return render(request, "feed.html", {
            'publicaciones': publicaciones,
            'user': request.user
    })

def search_users(request):
    query = request.GET.get('q', '')

    if query:
        users = User.objects.filter(username__icontains=query)[:10]

        data = []
        for user in users:
            perfil = getattr(user, 'perfil', None)

            data.append({
                'username': user.username,
                'id': user.id,
                'foto': perfil.foto_perfil.url if perfil and perfil.foto_perfil else None
            })
    else:
        data = []

    return JsonResponse(data, safe=False)
