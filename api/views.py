from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import requests
import os

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def auth(request):
	# redirect to the auth page
	AUTH_SERVICE_URL = f'{os.environ.get("AUTH_SERVICE_URL")}/v1/signin'
	return HttpResponseRedirect(AUTH_SERVICE_URL)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def signedin(request):
	pass

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
	EVENTS_SERVICE_URL = f'{os.environ.get("EVENTS_SERVICE_URL")}/v1/events'
	if request.method == 'GET':
		response = requests.get(EVENTS_SERVICE_URL, params=request.query_params)
		return Response(response.json(), status=response.status_code)
	
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def events_edit(request, event_id):
	EVENTS_SERVICE_URL = f'{os.environ.get("EVENTS_SERVICE_URL")}/v1/events/{event_id}'
	if request.method == 'POST':
		response = requests.post(EVENTS_SERVICE_URL, data=request.data)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'PATCH':
		response = requests.patch(EVENTS_SERVICE_URL, data=request.data)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'DELETE':
		response = requests.delete(EVENTS_SERVICE_URL)
		return Response(response.json(), status=response.status_code)

@api_view(['GET', 'PATCH'])
@permission_classes((AllowAny,))
@csrf_exempt
def points(request):
	POINTS_SERVICE_URL = f'{os.environ.get("POINTS_SERVICE_URL")}/v1/points'
	if request.method == 'GET':
		response = requests.get(POINTS_SERVICE_URL, params=request.query_params)
		return Response(response.json(), status=response.status_code)
	elif request.method == 'PATCH':
		response = requests.patch(POINTS_SERVICE_URL, data=request.data)
		return Response(response.json(), status=response.status_code)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def standings(request):
	STANDINGS_SERVICE_URL = f'{os.environ.get("POINTS_SERVICE_URL")}/v1/standings'
	response = requests.get(STANDINGS_SERVICE_URL)
	return Response(response.json(), status=response.status_code)