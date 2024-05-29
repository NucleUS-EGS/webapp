from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.logout, name='logout'),
    path('standings/', views.standings, name='standings'),
	path('students/', views.students, name='students'),
]