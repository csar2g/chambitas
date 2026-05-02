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
		img.src = user.foto || "/static/default.png";  // fallback
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
});
console.log("JS cargado");
