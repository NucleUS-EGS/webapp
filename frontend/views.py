from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import requests
import logging


logger = logging.getLogger(__name__)

import app.settings as settings

def build_url(request, service, path):
	scheme = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
	return f'{scheme}://{service}{path}'

def check_login(request):
	# get cookie value for AUTH_SERVICE_EMAIL
	step = request.COOKIES.get('AUTH_SERVICE_STEP', None)
	token = request.COOKIES.get('AUTH_SERVICE_ACCESS_TOKEN', None)
	points = get_points(request)	


	if token:
		user = get_user(request, token)
		logger.debug(f"user: {user}")

		if user and not 'error' in user:
			return {'id': user["id"], 'mail': user["email"], 'username': user["email"].split("@")[0], 'step': step, 'points': points, 'nucleo': user["nucleo"], 'user': user}
	
	student_nucleo = request.COOKIES.get('NUCLEO', None)
	mail = request.COOKIES.get('AUTH_SERVICE_EMAIL', None)
	return {'mail': mail, 'step': step, 'points': points, 'id': id, 'student_nucleo': student_nucleo}


def index(request):
	context = check_login(request)

	if not context['mail']:
		return HttpResponseRedirect('/login')
	
	if 'step' in context and context['step'] == 'register':
		return HttpResponseRedirect('/register')
	

	
	# get user id where email = mail
	context["events"] = requests.get(build_url(request, settings.API_URL, '/events')).json()
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
			
			# make post request with data
			response = requests.post(build_url(request, settings.API_URL, '/nucleossignin/'), json=data)
			print(response.status_code)
			if response.status_code == 200:
				response = response.json()
				nucleo_email = response.get('email')
				nucleo = nucleo_email.split('@')[0].upper()
				nucleo_id = response.get('id')

				
				response = HttpResponseRedirect('/')
				response.set_cookie('AUTH_SERVICE_EMAIL', nucleo_email)
				response.set_cookie('AUTH_SERVICE_STEP', 'loggedin')
				response.set_cookie('NUCLEO_ID', nucleo_id)
				response.set_cookie('NUCLEO', nucleo)
				
				return response
			else:
				return HttpResponseRedirect('/login')
		else:
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
			nucleo = get_nucleos(request)
			
			return HttpResponseRedirect(f'/api/v1/auth?mode=register')

		# nucleos = requests.get(build_url(request, settings.API_URL, '/nucleos')).json()
		context['nucleos'] = get_nucleos(request)
		return render(request, 'register.html', context)
	

def logout(request):
	response = HttpResponseRedirect('/')
	response.delete_cookie('AUTH_SERVICE_EMAIL')
	response.delete_cookie('AUTH_SERVICE_STEP')
	response.delete_cookie('AUTH_SERVICE_ACCESS_TOKEN')
	response.delete_cookie('AUTH_SERVICE_ID')
	response.delete_cookie('AUTH_SERVICE_USERNAME')
	response.delete_cookie('NUCLEO') 
	return response

def standings(request):
	context = check_login(request)

	context["standings"] = requests.get(build_url(request, settings.API_URL, '/standings')).json()

	return render(request, 'standings.html', context)


def students(request):
	context = check_login(request)
	nucleo_id = request.COOKIES.get('NUCLEO_ID', None)
	students_data = get_nucleo_students(request, nucleo_id)

	context['students'] = [
	{"email": student["email"], "points": get_points(request, student["id"]), "id": student["id"]}
	for student in students_data["users"]
	]

	return render(request, 'students.html', context)


def get_points(request, id=None):

	if id:
		url = build_url(request, settings.API_URL, f'/entity/?entity_id={id}')
		response = requests.get(url).json()
	
		if response and isinstance(response, list) and len(response) > 0:
			points = response[0].get('POINTS', 0)
	
		else:
			points = 0


		print(f"Points: {points} for user {id}")
	else:
		points = 0

	return points


# returns a list of all nucleos
def get_nucleos(request):
	url = build_url(request, settings.API_URL, f'/nucleos')
	response = requests.get(url).json()
	nucleos = response.get('nucleus', [])

	return nucleos


def get_user(request, token):
	url = build_url(request, settings.API_URL, f'/user?access_token={token}')
	response = requests.get(url).json()

	return response

# returns the users bellonging to that nucleo

def get_nucleo_students(request, nucleo_id):


	url = build_url(request, settings.API_URL, f'/students/{nucleo_id}')
	response = requests.get(url).json()
	
	return response