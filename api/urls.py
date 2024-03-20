from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

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
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

	# login
	path('auth/', views.auth, name='auth'),

	# user info
	path('user/', views.user, name='user'),

	# events
	path('events/', views.events, name='events'),
	path('events/<int:event_id>', views.events_edit, name='events'),

	# points
	path('points/', views.points, name='points'),

	# standings
	path('standings/', views.standings, name='standings'),
]