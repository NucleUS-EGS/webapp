from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 

import requests
import base64 
import re
import json

import logging
from django.conf import settings
from django.http import JsonResponse

import app.settings as settings

from .models import Institution
from django.forms.models import model_to_dict

logger = logging.getLogger(__name__)

def build_url_redirect(request, service, path):
	scheme = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
	host = request.META.get('HTTP_X_FORWARDED_HOST', 'localhost')
	port = request.META.get('PORT', '8000')
	service = re.sub(r':.*?/', '/', service)
	return f'{scheme}://{host}:{port}/{service}{path}'

def build_url(request, service, path):
	scheme = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
	return f'{scheme}://{service}{path}'

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def auth(request):
	encoded_key = base64.b64encode(settings.AUTH_SERVICE_KEY.encode("utf-8")).decode("utf-8")
	mode = request.query_params.get('mode')
	if mode:
		path = f'/{mode}?token={encoded_key}&institution={request.query_params.get("institution")}'
		url = build_url_redirect(request, settings.AUTH_SERVICE_URL, path)
		return HttpResponseRedirect(f'{url}')
	else:
		return Response({'error': 'Missing mode parameter'}, status=400)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def user(request):
	token = request.query_params.get('access_token')
	url = build_url(request, settings.AUTH_SERVICE_URL, '/user?access_token=' + token)
	response = requests.get(url, headers={
		'API_KEY': settings.AUTH_SERVICE_KEY,
		'Authorization': token
	})
	return Response(response.json(), status=response.status_code)


# @swagger_auto_schema(method='get', manual_parameters=[
#     openapi.Parameter('query', openapi.IN_QUERY, description='Query string', type=openapi.TYPE_STRING),
#     openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
#     openapi.Parameter('date_from', openapi.IN_QUERY, description='Date from', type=openapi.TYPE_STRING),
#     openapi.Parameter('date_to', openapi.IN_QUERY, description='Date to', type=openapi.TYPE_STRING),
# ])

#register page
@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def register(request):
	url = build_url(request, settings.AUTH_SERVICE_URL, '/register')
	response = requests.post(url, json=json.loads(request.body.decode('utf-8')), headers={
		'API_KEY': settings.AUTH_SERVICE_KEY,
	})
	return Response(response.json(), status=response.status_code)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def events(request):
	url = build_url(request, settings.EVENTS_SERVICE_URL, '/events')
	if request.method == 'GET':
		response = requests.get(url, params=request.query_params, headers={
			'API_KEY': settings.EVENTS_SERVICE_KEY
		})
		return Response(response.json(), status=response.status_code)
	
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def events_edit(request, event_id):
	url = build_url(request, settings.EVENTS_SERVICE_URL, f'/events/{event_id}')
	headers = {
		'API_KEY': settings.EVENTS_SERVICE_KEY,
	}
	if request.method == 'POST':
		response = requests.post(url, data=json.loads(request.body), headers=headers)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'PATCH':
		response = requests.patch(url, data=json.loads(request.body), headers=headers)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'DELETE':
		response = requests.delete(url, headers=headers)
		return Response(response.json(), status=response.status_code)


@api_view(['GET', 'PATCH'])
@permission_classes((AllowAny,))
@csrf_exempt
def points(request):
	# v1//entity?id=1
	url = build_url(request, settings.POINTS_SERVICE_URL, '/entity')
	entity_id = request.query_params.get('entity_id', None)

	if entity_id:
		url = f'{url}?id={entity_id}'

	headers = {
		'API_KEY': settings.POINTS_SERVICE_KEY,
	}
	if request.method == 'GET':
		response = requests.get(url, params=request.query_params, headers=headers)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'PATCH':
		response = requests.patch(url, data=json.loads(request.body), headers=headers)
		return Response(response.json(), status=response.status_code)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def standings(request):
	url = build_url(request, settings.POINTS_SERVICE_URL, '/standings')
	response = requests.get(url, headers={
		'API_KEY': settings.POINTS_SERVICE_KEY
	})
	return Response(response.json(), status=response.status_code)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def institutions(request):
	query = request.query_params.get('q')
	if query:
		institutions = Institution.objects.filter(name__icontains=query)
	else:
		institutions = Institution.objects.all()

	return Response([model_to_dict(institution) for institution in institutions])


# get list of nucleos
@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def nucleos(request):
	# make get request to auth service /nucleos
	url = build_url(request, settings.AUTH_SERVICE_URL, '/nucleus')
	response = requests.get(url, headers={
		'API_KEY': settings.AUTH_SERVICE_KEY
	})
	return Response(response.json(), status=response.status_code)

# post to create a new nucleo (sigin)
@api_view(['POST'])
@permission_classes((AllowAny,))
@csrf_exempt
def nucleossignin(request):

	url = build_url(request, settings.AUTH_SERVICE_URL, '/signin')
	response = requests.post(url, json=json.loads(request.body), headers={
		'API_KEY': settings.AUTH_SERVICE_KEY,
		'Content-Type': 'application/json'
	})
	content_type = response.headers.get('Content-Type', '')

	if 'application/json' in content_type:
		response_data = response.json()

	return Response(response_data, status=response.status_code)
    

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def nucleo_students(request, nucleo_id):
	# make get request to auth service /nucleos
	url = build_url(request, settings.AUTH_SERVICE_URL, f'/students?nucleo_id={nucleo_id}')
	response = requests.get(url, headers={
		'API_KEY': settings.AUTH_SERVICE_KEY
	})
	return Response(response.json(), status=response.status_code)

