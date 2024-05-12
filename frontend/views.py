from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import requests

import logging
logger = logging.getLogger(__name__)

def check_login(request):
	# get cookie value for AUTH_SERVICE_EMAIL
	mail = request.COOKIES.get('AUTH_SERVICE_EMAIL', None)
	step = request.COOKIES.get('AUTH_SERVICE_STEP', None)
	id = request.COOKIES.get('AUTH_SERVICE_ID')
	
	return {'mail': mail, 'step': step, 'id': id}

def index(request):
	context = check_login(request)

	if not context['mail']:
		return HttpResponseRedirect('/login')
	
	if 'step' in context and context['step'] == 'register':
		return HttpResponseRedirect('/register')


	context['points'] = points(request)
	context['standings'] = standings(request)

	
	# get user id where email = mail
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
	response.delete_cookie('AUTH_SERVICE_ID')
	return response


def points(request):

	id = request.COOKIES.get('AUTH_SERVICE_ID')
	if id:
		url = f'http://{request.get_host()}/api/v1/entity/?entity_id={id}'
		response = requests.get(url).json()
	
		if response and isinstance(response, list) and len(response) > 0:
			points = response[0].get('POINTS', 0)
	
		else:
			points = 0


		print(f"Points: {points} for user {id}")
	else:
		points = 0


	return points

def standings(request):

	mail = request.COOKIES.get('AUTH_SERVICE_EMAIL', None)
	step = request.COOKIES.get('AUTH_SERVICE_STEP', None)
	user_points = points(request)
	response = requests.get(f'http://{request.get_host()}/api/v1/standings').json()

	return render(request, 'standings.html', {'standings': response, 'mail': mail, 'step': step, 'points': user_points})