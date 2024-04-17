from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import requests

def check_login(request):
	# get cookie value for AUTH_SERVICE_EMAIL
	mail = request.COOKIES.get('AUTH_SERVICE_EMAIL', None)
	step = request.COOKIES.get('AUTH_SERVICE_STEP', None)
	return {'mail': mail, 'step': step}

def index(request):
	context = check_login(request)

	if not context['mail']:
		return HttpResponseRedirect('/login')
	
	if 'step' in context and context['step'] == 'register':
		return HttpResponseRedirect('/register')
	
	return render(request, 'index.html', context)
	

@csrf_exempt
def login(request):
	context = check_login(request)

	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		if email and password:
			# put in form data
			data = {
				'email': email,
				'password': password
			}
			# send post request to auth service
			# TODO

		institution = request.POST.get('institution')
		return HttpResponseRedirect(f'/api/v1/auth?institution={institution}&mode=signin')
	else:
		print(context)
		if context['mail']:
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html', context)


def register(request):
	context = check_login(request)

	if 'step' in context and context['step'] != 'register':
		return HttpResponseRedirect('/')

	# get cookie value for AUTH_SERVICE_EMAIL
	if not context['mail']:
		return HttpResponseRedirect('/login')
	else:
		if request.method == 'POST':
			nucleo = request.POST.get('nucleo')
			# put in form data
			data = {
				'nucleo': nucleo
			}
			return HttpResponseRedirect(f'/api/v1/auth?mode=register')

		nucleos = requests.get(f'http://{request.get_host()}/api/v1/nucleos?institution=2').json()
		context['nucleos'] = nucleos
		print(context)
		return render(request, 'register.html', context)
	

def logout(request):
	response = HttpResponseRedirect('/')
	response.delete_cookie('AUTH_SERVICE_EMAIL')
	response.delete_cookie('AUTH_SERVICE_STEP')
	response.delete_cookie('AUTH_SERVICE_ACCESS_TOKEN')
	return response