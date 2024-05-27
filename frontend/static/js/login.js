// Function to perform the search
const search = input => {
	const results = document.querySelector('.results');

	if (results) {
		results.innerHTML = '';

		if (input.length > 0) {
			// make request to api
			fetch(`${window.location.origin}/api/v1/institutions?q=${input}`)
				.then(response => response.json())
				.then(data => {
					data.forEach(item => {
						const result = document.createElement('div');
						result.classList.add('result');
						result.innerHTML = `
							<div class="logo"><img src="${STATIC_URL + item.logo}" alt="${item.name}"></div>
							<div>${item.name}</div>
							<input type="hidden" value="${item.id}">
						`;
						results.appendChild(result);

						result.addEventListener('click', () => {
							document.querySelectorAll('.result.active').forEach(result => {
								result.classList.remove('active');
								result.querySelector('input').removeAttribute('name');
							});

							result.classList.add('active');
							result.querySelector('input').setAttribute('name', 'institution');
							
							const idpButton = document.querySelector('.idp');
							idpButton.classList.remove('inactive');
							idpButton.value = item.text;
							idpButton.style.backgroundColor = item.color;
							idpButton.style.color = "#fff";
						});
					});
				});
		}

	}
};

const select = elem => {
	elem.parentElement.querySelectorAll('.active').forEach(item => {
		item.classList.remove('active');
		item.querySelector('input').removeAttribute('name');
	});

	elem.classList.toggle('active');
	elem.querySelector('input').setAttribute('name', 'nucleo');
	
	const button = document.querySelector('.buttons input[type="submit"]');
	if (button) {
		button.classList.remove('inactive');
	}
};

document.addEventListener('input', e => {
	const nucleo = e.target.closest('#nucleo-signin');
	if (nucleo) {
		const inputs = nucleo.querySelectorAll('input');
		console.log(inputs);
		if (Array.from(inputs).every(input => input.value)) {
			const button = document.querySelector('.buttons input[type="submit"]');
			button.classList.remove('inactive');
		}
		else {
			const button = document.querySelector('.buttons input[type="submit"]');
			button.classList.add('inactive');
		}
	}

	if (e.target.matches('input[name="email"], input[name="password"]')) {
		const loginButton = document.querySelector('.buttons .login_nucleo');
		if (e.target.value.length > 0) {
			loginButton.classList.remove('inactive');
			loginButton.style.backgroundColor = 'var(--light-gray)';
			loginButton.style.color = '#000'; 
		} else {
			loginButton.classList.add('inactive');
			loginButton.style.backgroundColor = ''; 
			loginButton.style.color = ''; 
		}
	}
});

window.addEventListener('load', () => {
	const uni = 'Universidade de Aveiro';
	search(uni);
	
	document.querySelector('input[name="email"]').value = '';
	document.querySelector('input[name="password"]').value = '';

});
