from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversacion, Mensaje
from users.models import Usuario


def _usuario_actual(request):
    return get_object_or_404(Usuario, auth_user=request.user)


@login_required
def bandeja(request):
    usuario = _usuario_actual(request)
    conversaciones_raw = Conversacion.objects.filter(
        usuario_emisor=usuario
    ) | Conversacion.objects.filter(
        usuario_receptor=usuario
    )
    conversaciones_raw = conversaciones_raw.order_by('-created_at')
    conversaciones = []
    for conv in conversaciones_raw:
        otro = conv.usuario_receptor if conv.usuario_emisor == usuario else conv.usuario_emisor
        ultimo = conv.mensajes.last()
        conversaciones.append({'conv': conv, 'otro': otro, 'ultimo_msg': ultimo})
    return render(request, 'message/message.html', {
        'usuario': usuario,
        'conversaciones': conversaciones,
        'conversacion_activa': None,
        'mensajes': [],
        'otro_header': None,
        'usuario_mensajes_id': usuario.id,
    })


@login_required
def conversacion(request, conversacion_id):
    usuario = _usuario_actual(request)
    conv_activa = get_object_or_404(
        Conversacion.objects.filter(id=conversacion_id).filter(
            usuario_emisor=usuario
        ) | Conversacion.objects.filter(id=conversacion_id).filter(
            usuario_receptor=usuario
        )
    )

    # ← ENVÍO DE MENSAJE
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Mensaje.objects.create(
                conversacion=conv_activa,
                usuario_emisor=usuario,
                contenido=contenido,
            )
        return redirect('conversacion', conversacion_id=conversacion_id)

    mensajes = conv_activa.mensajes.all()
    conversaciones_raw = Conversacion.objects.filter(
        usuario_emisor=usuario
    ) | Conversacion.objects.filter(
        usuario_receptor=usuario
    )
    conversaciones_raw = conversaciones_raw.order_by('-created_at')
    conversaciones = []
    for conv in conversaciones_raw:
        otro = conv.usuario_receptor if conv.usuario_emisor == usuario else conv.usuario_emisor
        ultimo = conv.mensajes.last()
        conversaciones.append({'conv': conv, 'otro': otro, 'ultimo_msg': ultimo})
    otro_header = conv_activa.usuario_receptor if conv_activa.usuario_emisor == usuario else conv_activa.usuario_emisor
    return render(request, 'message/message.html', {
        'usuario': usuario,
        'conversaciones': conversaciones,
        'conversacion_activa': conv_activa,
        'mensajes': mensajes,
        'otro_header': otro_header,
        'usuario_mensajes_id': usuario.id,
    })