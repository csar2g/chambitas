function toggleComentarios(pubId) {
    const section = document.getElementById(`comentarios-${pubId}`);
    section.classList.toggle('hidden');
    if (!section.classList.contains('hidden')) {
        document.getElementById(`input-comentario-${pubId}`)?.focus();
    }
}

function enviarComentario(pubId) {
    const input = document.getElementById(`input-comentario-${pubId}`);
    const contenido = input.value.trim();
    if (!contenido) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/publicacion/${pubId}/comentar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: `contenido=${encodeURIComponent(contenido)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) return;

        // Elimina el mensaje "No hay comentarios" si existe
        const empty = document.getElementById(`empty-${pubId}`);
        if (empty) empty.remove();

        // Inserta el nuevo comentario en la lista
        const lista = document.getElementById(`lista-comentarios-${pubId}`);
        const foto = data.foto
            ? `<img src="${data.foto}" class="w-full h-full object-cover">`
            : `<img src="/static/img/default.jpg" class="w-full h-full object-cover">`;

		lista.insertAdjacentHTML('beforeend', `
			<div class="flex gap-3 items-start">
				<a href="/perfil/${data.user_id}/" class="w-8 h-8 rounded-full overflow-hidden shrink-0 hover:opacity-80 transition-opacity">${foto}</a>
				<div class="bg-surface-container rounded-2xl px-4 py-2 flex-1">
					<div class="flex items-baseline gap-2">
						<a href="/perfil/${data.user_id}/" class="text-sm font-bold text-on-surface hover:underline">${data.username}</a>
						<p class="text-[10px] text-on-surface-variant">Hace ${data.created_at}</p>
					</div>
					<p class="text-sm text-on-surface-variant">${data.contenido}</p>
				</div>
			</div>
		`);
        // Actualiza el contador de comentarios
        const contadores = document.querySelectorAll(`[data-comments="${pubId}"]`);
        contadores.forEach(el => {
            const actual = parseInt(el.textContent) || 0;
            el.textContent = actual + 1;
        });

        input.value = '';
    });
}
