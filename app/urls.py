"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method="get", auto_schema=None)
@api_view(['GET'])
def skip(request):
    pass

schema_view = get_schema_view(
	openapi.Info(
		title="NucleUS",
		default_version='v1',
		description="NucleUS API",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	# swagger docs
    re_path(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	
    path('django/admin/', admin.site.urls, name='admin'),
    
    # api
	path('api/v1/', include('api.urls')),
	
    # dummy endpoint to help swagger generate the schema
    path('api/skip', skip, name='skip'),

    # frontend
    path('', include('frontend.urls')),
]