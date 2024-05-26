from django.db import models

class User(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.EmailField()

class UserEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.IntegerField()

class UserPoints(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.IntegerField()

class UserAuth(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.IntegerField()

class Institution(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	logo = models.CharField(max_length=255)
	color = models.CharField(max_length=255)
	text = models.CharField(max_length=255)

class Nucleo(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	short = models.CharField(max_length=255)
	logo = models.CharField(max_length=255)
	institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

class NucleoAuth(models.Model):
	id = models.AutoField(primary_key=True)
	mail = models.EmailField()
	password = models.CharField(max_length=255)