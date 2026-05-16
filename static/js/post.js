let imagenesSeleccionadas = [];

console.log("Post cargado")

document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('form-publicacion');
	if (!form) return
    form.addEventListener('submit', function(e) {
        const input = document.getElementById('input-imagen');

        const dataTransfer = new DataTransfer();

        imagenesSeleccionadas.forEach(file => {
            dataTransfer.items.add(file);
        });

        input.files = dataTransfer.files;

        console.log("Enviando:", dataTransfer.files.length); 
    });
});
function abrirModal() {
    document.getElementById('modal-post').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-post').classList.add('hidden');
}

function previewImagen(event) {
    const contenedor = document.getElementById('contenedor-imagenes');

    Array.from(event.target.files).forEach(file => {

        imagenesSeleccionadas.push(file);

        const url = URL.createObjectURL(file);

        const div = document.createElement('div');
        div.className = "relative";

        div.innerHTML = `
            <img src="${url}" class="w-24 h-24 object-cover rounded">
            <button type="button"
                class="absolute top-1 right-1 bg-black/60 text-white w-5 h-5 rounded-full flex items-center justify-center">
                ✕
            </button>
        `;

        div.querySelector('button').onclick = () => {
            imagenesSeleccionadas = imagenesSeleccionadas.filter(f => f !== file);
            div.remove();
        };

        contenedor.appendChild(div);
    });

    event.target.value = "";
}

window.verImagen = function(src) {
    const modal = document.getElementById('modal-img');
    const img = document.getElementById('img-grande');

    img.src = src;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

window.cerrarImagen = function() {
    const modal = document.getElementById('modal-img');
    modal.classList.add('hidden');
}

function darLike(id, btn) {
    fetch(`/like/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {

        const contador = btn.closest('article')
            .querySelector('.contador-reacciones');

        contador.innerText = data.total + " reactions";
	
		const icon = btn.querySelector('.material-symbols-outlined');
		const texto = btn.querySelector('.texto-like');

		if (data.liked) {
		btn.classList.remove('text-on-surface-variant');
		btn.classList.add('text-blue-600');

		icon.style.fontVariationSettings = "'FILL' 1";
		texto.innerText = "Liked";

		} else {
		btn.classList.remove('text-blue-600');
		btn.classList.add('text-on-surface-variant'); 

		icon.style.fontVariationSettings = "'FILL' 0";
		texto.innerText = "Like";
		}
	});
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        .split('=')[1];
}

function mostrarLink() {
    document.getElementById('contenedor-link').classList.remove('hidden');
    document.getElementById('btn-link').classList.add('hidden');
    document.getElementById('input-link').focus();
}

function quitarLink() {
    document.getElementById('contenedor-link').classList.add('hidden');
    document.getElementById('btn-link').classList.remove('hidden');
    document.getElementById('input-link').value = '';
}
