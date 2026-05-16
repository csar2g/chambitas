	let _editandoId = null;

			function toggleMenu(id) {
				document.querySelectorAll('[id^="menu-"]').forEach(m => {
					if (m.id !== `menu-${id}`) m.classList.add('hidden');
				});
				document.getElementById(`menu-${id}`).classList.toggle('hidden');
			}

			function abrirEditar(id, descripcion) {
				_editandoId = id;
				document.getElementById('textarea-editar').value = descripcion;
				document.getElementById('modal-editar').classList.remove('hidden');
				document.getElementById(`menu-${id}`).classList.add('hidden');
			}

			function cerrarEditar() {
				document.getElementById('modal-editar').classList.add('hidden');
			}

			async function guardarEdicion() {
				const desc = document.getElementById('textarea-editar').value.trim();
				if (!desc) return;
				const res = await fetch(`/publicacion/${_editandoId}/editar/`, {
					method: 'POST',
					headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/x-www-form-urlencoded'},
					body: `descripcion=${encodeURIComponent(desc)}`
				});
				if (res.ok) location.reload();
			}

			function confirmarEliminar(id) {
				document.getElementById('modal-eliminar').classList.remove('hidden');
				document.getElementById('btn-confirmar-eliminar').onclick = async () => {
					const res = await fetch(`/publicacion/${id}/eliminar/`, {
						method: 'POST',
						headers: {'X-CSRFToken': getCSRFToken()}
					});
					if (res.ok) location.reload();
				};
			}



function abrirEditar(id, descripcion, link, imagenes) {
    document.getElementById('modal-editar').classList.remove('hidden');
    document.getElementById('textarea-editar').value = descripcion;
    document.getElementById('form-editar').action = `/publicacion/${id}/editar/`;

    // Link
    const contenedorLink = document.getElementById('contenedor-link-editar');
    const inputLink = document.getElementById('input-link-editar');
    const btnLink = document.getElementById('btn-link-editar');
    if (link) {
        inputLink.value = link;
        contenedorLink.classList.remove('hidden');
        btnLink.classList.add('hidden');
    } else {
        inputLink.value = '';
        contenedorLink.classList.add('hidden');
        btnLink.classList.remove('hidden');
    }

    // Imágenes actuales
    const contenedor = document.getElementById('imagenes-actuales');
    contenedor.innerHTML = '';
    if (imagenes && imagenes.length > 0) {
        imagenes.forEach(img => {
            const div = document.createElement('div');
            div.className = 'relative';
            div.innerHTML = `
                <img src="${img.url}" class="w-24 h-24 object-cover rounded-lg border border-outline-variant/20">
                <input type="hidden" name="eliminar_imagen" value="${img.id}" disabled id="del-${img.id}">
                <button type="button" onclick="marcarEliminarImagen(${img.id}, this)"
                    class="absolute top-1 right-1 bg-black/60 text-white w-5 h-5 rounded-full flex items-center justify-center text-xs">
                    ✕
                </button>
            `;
            contenedor.appendChild(div);
        });
    }

    // Limpiar preview nuevas imágenes
    document.getElementById('preview-imagenes-editar').innerHTML = '';
    document.getElementById('input-imagen-editar').value = '';

    document.querySelectorAll('[id^="menu-"]').forEach(m => m.classList.add('hidden'));
}

function marcarEliminarImagen(imgId, btn) {
    const input = document.getElementById(`del-${imgId}`);
    const imgEl = btn.closest('.relative').querySelector('img');
    if (input.disabled) {
        input.disabled = false;
        imgEl.classList.add('opacity-30');
        btn.textContent = '↩';
        btn.classList.replace('bg-black/60', 'bg-primary');
    } else {
        input.disabled = true;
        imgEl.classList.remove('opacity-30');
        btn.textContent = '✕';
        btn.classList.replace('bg-primary', 'bg-black/60');
    }
}

function previewImagenEditar(event) {
    const contenedor = document.getElementById('preview-imagenes-editar');
    Array.from(event.target.files).forEach(file => {
        const url = URL.createObjectURL(file);
        const div = document.createElement('div');
        div.className = 'relative';
        div.innerHTML = `<img src="${url}" class="w-24 h-24 object-cover rounded-lg">`;
        contenedor.appendChild(div);
    });
}

function mostrarLinkEditar() {
    document.getElementById('contenedor-link-editar').classList.remove('hidden');
    document.getElementById('btn-link-editar').classList.add('hidden');
    document.getElementById('input-link-editar').focus();
}

function quitarLinkEditar() {
    document.getElementById('contenedor-link-editar').classList.add('hidden');
    document.getElementById('btn-link-editar').classList.remove('hidden');
    document.getElementById('input-link-editar').value = '';
}

function abrirEditar(id, descripcion, link, imagenes) {
    document.getElementById('modal-editar').classList.remove('hidden');
    document.getElementById('textarea-editar').value = descripcion;
    document.getElementById('form-editar').action = `/publicacion/${id}/editar/`;

    // Link
    const contenedorLink = document.getElementById('contenedor-link-editar');
    const inputLink = document.getElementById('input-link-editar');
    const btnLink = document.getElementById('btn-link-editar');
    if (link) {
        inputLink.value = link;
        contenedorLink.classList.remove('hidden');
        btnLink.classList.add('hidden');
    } else {
        inputLink.value = '';
        contenedorLink.classList.add('hidden');
        btnLink.classList.remove('hidden');
    }

    // Imágenes actuales
    const contenedor = document.getElementById('imagenes-actuales');
    contenedor.innerHTML = '';
    if (imagenes && imagenes.length > 0) {
        imagenes.forEach(img => {
            const div = document.createElement('div');
            div.className = 'relative';
            div.innerHTML = `
                <img src="${img.url}" class="w-24 h-24 object-cover rounded-lg border border-outline-variant/20">
                <input type="hidden" name="eliminar_imagen" value="${img.id}" disabled id="del-${img.id}">
                <button type="button" onclick="marcarEliminarImagen(${img.id}, this)"
                    class="absolute top-1 right-1 bg-black/60 text-white w-5 h-5 rounded-full flex items-center justify-center text-xs">
                    ✕
                </button>
            `;
            contenedor.appendChild(div);
        });
    }

    // Limpiar preview nuevas imágenes
    document.getElementById('preview-imagenes-editar').innerHTML = '';
    document.getElementById('input-imagen-editar').value = '';

    document.querySelectorAll('[id^="menu-"]').forEach(m => m.classList.add('hidden'));
}

function marcarEliminarImagen(imgId, btn) {
    const input = document.getElementById(`del-${imgId}`);
    const imgEl = btn.closest('.relative').querySelector('img');
    if (input.disabled) {
        input.disabled = false;
        imgEl.classList.add('opacity-30');
        btn.textContent = '↩';
        btn.classList.replace('bg-black/60', 'bg-primary');
    } else {
        input.disabled = true;
        imgEl.classList.remove('opacity-30');
        btn.textContent = '✕';
        btn.classList.replace('bg-primary', 'bg-black/60');
    }
}

function previewImagenEditar(event) {
    const contenedor = document.getElementById('preview-imagenes-editar');
    Array.from(event.target.files).forEach(file => {
        const url = URL.createObjectURL(file);
        const div = document.createElement('div');
        div.className = 'relative';
        div.innerHTML = `<img src="${url}" class="w-24 h-24 object-cover rounded-lg">`;
        contenedor.appendChild(div);
    });
}

function mostrarLinkEditar() {
    document.getElementById('contenedor-link-editar').classList.remove('hidden');
    document.getElementById('btn-link-editar').classList.add('hidden');
    document.getElementById('input-link-editar').focus();
}

function quitarLinkEditar() {
    document.getElementById('contenedor-link-editar').classList.add('hidden');
    document.getElementById('btn-link-editar').classList.remove('hidden');
    document.getElementById('input-link-editar').value = '';
}
