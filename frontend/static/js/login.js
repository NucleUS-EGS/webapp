const search = input => {
	const results = document.querySelector('.results');

	if (results) {
		results.innerHTML = '';

		if (input.length > 0) {
			// make request to api
			fetch(`http://127.0.0.1:3000/api/v1/institutions?q=${input}`)
				.then(response => response.json())
				.then(data => {
					data.forEach(item => {
						const result = document.createElement('div');
						result.classList.add('result');
						result.innerHTML = `
							<div class="logo"><img src="${STATIC_URL + item.logo}" alt="${item.name}"></div>
							<div>${item.name}</div>
						`;
						results.appendChild(result);

						result.addEventListener('click', () => {
							console.log(item);
							document.querySelectorAll('.result.active').forEach(result => result.classList.remove('active'));
							result.classList.add('active');
							
							const idpButton = document.querySelector('.idp');
							idpButton.classList.remove('inactive');
							idpButton.innerText = item.text;
							idpButton.style.backgroundColor = item.color;
							idpButton.style.color = "#fff";
						});
					});
				});
		}

	}

}