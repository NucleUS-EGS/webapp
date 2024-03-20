from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg.inspectors import BaseInspector, SwaggerAutoSchema

import requests

import app.settings as settings

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def auth(request):
	url = f'{settings.AUTH_SERVICE_URL}/v1/auth'
	return HttpResponseRedirect(url)


@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def user(request):
	token = request.headers.get('Authorization')
	url = f'{settings.AUTH_SERVICE_URL}/v1/user'
	response = requests.get(url, headers={
		'API-Key': settings.AUTH_SERVICE_KEY,
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
	url = f'{settings.EVENTS_SERVICE_URL}/v1/events'
	if request.method == 'GET':
		response = requests.get(url, params=request.query_params, headers={
			'API-Key': settings.EVENTS_SERVICE_KEY
		})
		return Response(response.json(), status=response.status_code)
	
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def events_edit(request, event_id):
	url = f'{settings.EVENTS_SERVICE_URL}/v1/events/{event_id}'
	headers = {
		'API-Key': settings.EVENTS_SERVICE_KEY,
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
	url = f'{settings.POINTS_SERVICE_URL}/v1/points'
	headers = {
		'API-Key': settings.POINTS_SERVICE_KEY,
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
	url = f'{settings.POINTS_SERVICE_URL}/v1/standings'
	response = requests.get(url, headers={
		'API-Key': settings.POINTS_SERVICE_KEY
	})
	return Response(response.json(), status=response.status_code)