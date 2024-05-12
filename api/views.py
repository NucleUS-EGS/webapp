from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 

import requests
import base64 

import app.settings as settings

from .models import Institution, Nucleo
from django.forms.models import model_to_dict

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def auth(request):
	encoded_key = base64.b64encode(settings.AUTH_SERVICE_KEY.encode("utf-8")).decode("utf-8")
	mode = request.query_params.get('mode')
	if mode:
		url = f'{settings.AUTH_SERVICE_URL}/{mode}?token={encoded_key}&institution={request.query_params.get("institution")}'
		return HttpResponseRedirect(f'{url}')
	else:
		return Response({'error': 'Missing mode parameter'}, status=400)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def user(request):
	token = request.headers.get('Authorization')
	url = f'{settings.AUTH_SERVICE_URL}/user'
	response = requests.get(url, headers={
		'API_KEY': settings.AUTH_SERVICE_KEY,
		'Authorization': token
	})
	return Response(response.json(), status=response.status_code)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('query', openapi.IN_QUERY, description='Query string', type=openapi.TYPE_STRING),
    openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
    openapi.Parameter('date_from', openapi.IN_QUERY, description='Date from', type=openapi.TYPE_STRING),
    openapi.Parameter('date_to', openapi.IN_QUERY, description='Date to', type=openapi.TYPE_STRING),
])
@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def events(request):
	url = f'{settings.EVENTS_SERVICE_URL}/events'
	if request.method == 'GET':
		response = requests.get(url, params=request.query_params, headers={
			'API_KEY': settings.EVENTS_SERVICE_KEY
		})
		return Response(response.json(), status=response.status_code)
	
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def events_edit(request, event_id):
	url = f'{settings.EVENTS_SERVICE_URL}/events/{event_id}'
	headers = {
		'API_KEY': settings.EVENTS_SERVICE_KEY,
	}
	if request.method == 'POST':
		response = requests.post(url, data=request.data, headers=headers)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'PATCH':
		response = requests.patch(url, data=request.data, headers=headers)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'DELETE':
		response = requests.delete(url, headers=headers)
		return Response(response.json(), status=response.status_code)


@api_view(['GET', 'PATCH'])
@permission_classes((AllowAny,))
@csrf_exempt
def points(request):
	url = f'{settings.POINTS_SERVICE_URL}/entity'

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
		response = requests.patch(url, data=request.data, headers=headers)
		return Response(response.json(), status=response.status_code)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def standings(request):
	url = f'{settings.POINTS_SERVICE_URL}/standings'
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


@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def nucleos(request):
	institution = request.query_params.get('institution')
	if institution:
		nucleos = Nucleo.objects.filter(institution__id=institution)
	else:
		nucleos = Nucleo.objects.all()
	
	return Response([model_to_dict(nucleo) for nucleo in nucleos])