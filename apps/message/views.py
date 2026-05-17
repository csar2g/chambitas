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
        imagen = request.FILES.get('file-input') or request.FILES.get('imagen')
        if contenido or imagen:
            Mensaje.objects.create(
                conversacion=conv_activa,
                usuario_emisor=usuario,
                contenido=contenido,
                imagen=imagen,
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

@login_required
def iniciar_conversacion(request, receptor_id):
    usuario = _usuario_actual(request)
    receptor = get_object_or_404(Usuario, auth_user_id=receptor_id)

    # No permitir conversación consigo mismo
    if receptor == usuario:
        return redirect('bandeja')

    # Buscar conversación existente
    conv = Conversacion.objects.filter(
        usuario_emisor=usuario, usuario_receptor=receptor
    ).first() or Conversacion.objects.filter(
        usuario_emisor=receptor, usuario_receptor=usuario
    ).first()

    if conv:
        return redirect('conversacion', conversacion_id=conv.id)

    # No existe → mostrar draft
    conversaciones_raw = (
        Conversacion.objects.filter(usuario_emisor=usuario) |
        Conversacion.objects.filter(usuario_receptor=usuario)
    ).order_by('-created_at')

    conversaciones = []
    for c in conversaciones_raw:
        otro = c.usuario_receptor if c.usuario_emisor == usuario else c.usuario_emisor
        ultimo = c.mensajes.last()
        conversaciones.append({'conv': c, 'otro': otro, 'ultimo_msg': ultimo})

    return render(request, 'message/message.html', {
        'usuario': usuario,
        'conversaciones': conversaciones,
        'conversacion_activa': None,
        'mensajes': [],
        'otro_header': receptor,
        'draft_receptor_id': receptor.auth_user_id,  # ← señal de modo draft
        'usuario_mensajes_id': usuario.id,
    })

@login_required
def crear_conversacion(request):
    if request.method != 'POST':
        return redirect('bandeja')

    usuario = _usuario_actual(request)
    receptor_id = request.POST.get('receptor_id')
    contenido = request.POST.get('contenido', '').strip()

    imagen = request.FILES.get('file-input') or request.FILES.get('imagen')
    if not receptor_id or (not contenido and not imagen):
        return redirect('bandeja')
    
    if not receptor_id or not contenido:
        return redirect('bandeja')

    receptor = get_object_or_404(Usuario, auth_user_id=receptor_id)

    # Doble check: si ya existe, solo enviar mensaje
    conv = Conversacion.objects.filter(
        usuario_emisor=usuario, usuario_receptor=receptor
    ).first() or Conversacion.objects.filter(
        usuario_emisor=receptor, usuario_receptor=usuario
    ).first()

    if not conv:
        conv = Conversacion.objects.create(
            usuario_emisor=usuario,
            usuario_receptor=receptor,
        )

    Mensaje.objects.create(
        conversacion=conv,
        usuario_emisor=usuario,
        contenido=contenido,
        imagen=imagen,
    )
    return redirect('conversacion', conversacion_id=conv.id)