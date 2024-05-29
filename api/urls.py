from django.urls import path

from . import views

urlpatterns = [
	# login
	path('auth/', views.auth, name='auth'),

	# for nucleos signin
    path('nucleossignin/', views.nucleossignin, name='nucleossignin'),
    
	# register
    path('register/', views.register, name='register'),
    
	# user info
	path('user/', views.user, name='user'),

	# events
	#path('events/', views.events, name='events'),
	path('events/', views.events, name='events'),

	# points
	path('entity/', views.points, name='entity'),
    
	# standings
	path('standings/', views.standings, name='standings'),

	# internal
	path('institutions/', views.institutions, name='institutions'),
	
	# nucleos students
 	path('students/<int:nucleo_id>/', views.nucleo_students, name='nucleo_students'),
    # for nucleos list
    path('nucleos/', views.nucleos, name='nucleos')
]