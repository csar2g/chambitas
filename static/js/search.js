const input = document.getElementById('search-input');
const results = document.getElementById('results');

input.addEventListener('keyup', async () => {
    const query = input.value;

    if (query.length === 0) {
        results.innerHTML = '';
        return;
    }

    const response = await fetch(`/search-users/?q=${query}`);
    const data = await response.json();

    results.innerHTML = '';

	data.forEach(user => {
		const div = document.createElement('div');
		div.className = "flex items-center gap-2 p-2 hover:bg-gray-200 cursor-pointer";

		const img = document.createElement('img');
		img.src = user.foto || "/static/img/default.jpg";  // fallback
		img.className = "w-8 h-8 rounded-full object-cover";

		const span = document.createElement('span');
		span.textContent = user.username;

		div.appendChild(img);
		div.appendChild(span);

		div.onclick = () => {
			window.location.href = `/perfil/${user.username}/`;
		};

		results.appendChild(div);
	});
	
	if (query.length > 0) {
		const verTodos = document.createElement('div');
		const buscarTexto = document.createElement('div');

		buscarTexto.innerHTML = `Buscar "<strong>${query}</strong>"`;

		buscarTexto.className = "p-2 text-sm text-gray-700 cursor-pointer hover:bg-gray-100";
		verTodos.className = "p-2 text-center text-emerald-600 font-semibold cursor-pointer hover:bg-gray-100 border-t";

		verTodos.textContent = "Ver todos los resultados";

		verTodos.onclick = () => {
			window.location.href = `/buscar/?q=${query}`;
		};

		buscarTexto.onclick = () => {
			window.location.href = `/buscar/?q=${query}`;
		};
		results.appendChild(buscarTexto);
		results.appendChild(verTodos);
	}
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); 
        window.location.href = `/buscar/?q=${input.value}`;
    }
});

console.log("JS cargado");
