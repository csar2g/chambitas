let imagenesSeleccionadas = [];

document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('form-publicacion');

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


