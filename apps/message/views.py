from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversacion, Mensaje
from users.models import Usuario

def bandeja(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
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
    })

def conversacion(request, usuario_id, conversacion_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    conv_activa = get_object_or_404(Conversacion, id=conversacion_id)

    # ← ENVÍO DE MENSAJE
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        #imagen = request.FILES.get('imagen')
        if contenido or imagen:
            Mensaje.objects.create(
                conversacion=conv_activa,
                usuario_emisor=usuario,
                contenido=contenido,
                #imagen=imagen,
            )
        return redirect('conversacion', usuario_id=usuario_id, conversacion_id=conversacion_id)

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
    })