from django.urls import path

from . import views

urlpatterns = [
	# login
	path('auth/', views.auth, name='auth'),

	# user info
	path('user/', views.user, name='user'),

	# events
	path('events/', views.events, name='events'),
	path('events/<int:event_id>', views.events_edit, name='events'),

	# points
	path('entity/', views.points, name='entity'),
    
	# standings
	path('standings/', views.standings, name='standings'),

	# internal
	path('institutions/', views.institutions, name='institutions'),
	path('nucleos/', views.nucleos, name='nucleos'),
]