document.addEventListener('DOMContentLoaded', (event) => {
    const resultsDiv = document.querySelector('.results');
    const submitButton = document.querySelector('.buttons input[type="submit"]');

    resultsDiv.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('result')) {
            document.querySelectorAll('.result').forEach(el => el.classList.remove('active'));
            e.target.classList.add('active');
            submitButton.classList.remove('inactive');
        }
    });

    document.querySelector('form.auth-container').addEventListener('submit', (e) => {
        e.preventDefault();
        const active = document.querySelector('.results .active');
        if (active) {
            const nucleoName = active.innerText.trim();
            console.log("selected:", nucleoName);
			console.log(JSON.stringify({ nucleo: nucleoName }));
            fetch(`${window.location.origin}/api/v1/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
					nucleo: nucleoName,
					access_token: getCookie("AUTH_SERVICE_ACCESS_TOKEN")
				})
            })
            .then(response => response.json())
            .then(data => {
                if (data.step === 'loggedin') {
                    document.cookie = "AUTH_SERVICE_STEP=loggedin; path=/";
                    window.location.href = '/';
                } else {
                    alert('fail');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while registering nucleo');
            });
        } else {
            alert('select a nucleo');
        }
    });
});

function getCookie(cname) {
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(';');
	for(let i = 0; i <ca.length; i++) {
	  let c = ca[i];
	  while (c.charAt(0) == ' ') {
		c = c.substring(1);
	  }
	  if (c.indexOf(name) == 0) {
		return c.substring(name.length, c.length);
	  }
	}
	return "";
  }