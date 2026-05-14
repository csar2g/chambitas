from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count
from .models import Publicacion, Reaccion, Comentario, ImagenPublicacion
from profiles.models import Perfil

@login_required(login_url='landing')
def feed_view(request):
    publicaciones = Publicacion.objects.all()\
        .annotate(total_reacciones=Count('reacciones'))\
        .order_by('-created_at')

    for pub in publicaciones:
        pub.liked = pub.reacciones.filter(user=request.user).exists()

    return render(request, "feed.html", {
        'publicaciones': publicaciones
    })

@require_POST
@login_required
def crear_publicacion(request):
    descripcion = request.POST.get('descripcion', '').strip()
    imagenes = request.FILES.getlist('imagen')

    if not descripcion:
        return redirect('feed')

    publicacion = Publicacion.objects.create(
        descripcion=descripcion,
        user=request.user
    )

    for img in imagenes:
        ImagenPublicacion.objects.create(
            publicacion=publicacion,
            imagen=img
        )

    print(len(request.FILES.getlist('imagen')))
    return redirect('feed')

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

@require_POST
@login_required
def toggle_like(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    like = Reaccion.objects.filter(
        user=request.user,
        publicacion=publicacion
    ).first()

    if like:
        like.delete()
        liked = False
    else:
        Reaccion.objects.create(
            user=request.user,
            publicacion=publicacion
        )
        liked = True

    return JsonResponse({
        'liked': liked,
        'total': publicacion.reacciones.count()
    })

def buscar_view(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'todo')
    usuarios = []
    publicaciones = []

    if query:
        if tipo in ('todo', 'usuarios'):
            usuarios = list(User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )[:4])
            for u in usuarios:
                perfil = getattr(u, 'perfil', None)
                if perfil and perfil.aptitudes:
                    u.aptitudes_lista = [a.strip() for a in perfil.aptitudes.split(',') if a.strip()]
                else:
                    u.aptitudes_lista = []

        if tipo in ('todo', 'publicaciones'):
            publicaciones = Publicacion.objects.filter(
                descripcion__icontains=query
            ).annotate(
                total_reacciones=Count('reacciones')
            ).order_by('-created_at')
            for pub in publicaciones:
                pub.liked = pub.reacciones.filter(user=request.user).exists()

    return render(request, 'results.html', {
        'usuarios': usuarios,
        'publicaciones': publicaciones,
        'query': query,
        'tipo': tipo,
    })

@require_POST
@login_required
def agregar_comentario(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    contenido = request.POST.get('contenido', '').strip()
    if not contenido:
        return JsonResponse({'error': 'Comentario vacío'}, status=400)
    comentario = Comentario.objects.create(
        contenido=contenido,
        user=request.user,
        publicacion=publicacion
    )
    perfil = getattr(comentario.user, 'perfil', None)
    return JsonResponse({
        'id': comentario.id,
        'contenido': comentario.contenido,
        'username': comentario.user.get_full_name() or comentario.user.username,
        'foto': perfil.foto_perfil.url if perfil and perfil.foto_perfil else None,
        'created_at': timesince(comentario.created_at),
    })

@require_POST
@login_required
def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id, user=request.user)
    descripcion = request.POST.get('descripcion', '').strip()
    if descripcion:
        publicacion.descripcion = descripcion
        publicacion.save()
    return JsonResponse({'descripcion': publicacion.descripcion})

@require_POST
@login_required
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id, user=request.user)
    # Eliminar imágenes del storage
    for img in publicacion.imagenes.all():
        img.imagen.delete()
    publicacion.delete()
    return JsonResponse({'ok': True})
