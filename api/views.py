from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

import requests
import base64
import os

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def auth(request):
	# redirect to the auth page
	AUTH_SERVICE_URL = f'{os.environ.get('AUTH_SERVICE_URL')}/v1/signin'
	return HttpResponseRedirect(AUTH_SERVICE_URL)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def signedin(request):
	pass