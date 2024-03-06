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
	url=f'{os.environ.get("UA_IDP_URL")}/{os.environ.get("UA_IDP_AUTH_ENDPOINT")}'

	CLIENT_ID = os.environ.get('UA_IDP_CLIENT_ID')
	params = {
		'response_type': 'code',
		'client_id': CLIENT_ID,
		'redirect_uri': 'http://localhost:3000',
		'scope': 'openid',
		'state': 'sahfiewhfilwhe'
	}
	
	# make it through url redirect
	redirect_url = url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
	return HttpResponseRedirect(redirect_url)

@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def callback(request):
	CLIENT_ID = os.environ.get('UA_IDP_CLIENT_ID')
	CLIENT_SECRET = os.environ.get('UA_IDP_CLIENT_SECRET')
	byte_data = f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')
	encoded = base64.b64encode(byte_data).decode('utf-8')

	print("code:")
	print(request.query_params['code'])
	print("encoded:")
	print(encoded)
	print("####")

	url=f'{os.environ.get("UA_IDP_URL")}/{os.environ.get("UA_IDP_TOKEN_ENDPOINT")}'
	headers = {
		'Authorization': f'Basic {encoded}',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	
	code = request.query_params['code']
	params = {
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': 'http://localhost:3000'
	}

	# make post request
	response = requests.post(url, headers=headers, params=params)
	
	if response.status_code == 200:
		result = {}

		result["private"] = response.json()

		print(result)

		token_type = result["private"]["token_type"]
		access_token = result["private"]["access_token"]

		url=f'{os.environ.get("UA_IDP_URL")}/{os.environ.get("UA_IDP_USERINFO_ENDPOINT")}'
		headers = {
			'Authorization': f'{token_type} {access_token}'
		}
		user_data = requests.get(url, headers=headers)
		
		result["public"] = user_data.json()
		return Response(result, status=status.HTTP_200_OK)

	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)