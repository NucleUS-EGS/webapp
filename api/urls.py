from django.urls import path

from . import views

urlpatterns = [
	# login
	path('auth/', views.auth, name='auth'),

	# user info
	path('user/', views.user, name='user'),

	# events
	#path('events/', views.events, name='events'),
	path('events/', views.events_edit, name='events'),

	# points
	path('entity/', views.points, name='entity'),
    
	# standings
	path('standings/', views.standings, name='standings'),

	# internal
	path('institutions/', views.institutions, name='institutions'),
	

	#for nucleos signin
    path('nucleossignin/', views.nucleossignin, name='nucleossignin'),
    
    #for nucleos list
    path('nucleos/', views.nucleos, name='nucleos')
]