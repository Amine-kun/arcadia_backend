from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.password_validation import validate_password


class Users(models.Model):
	id = models.AutoField(primary_key=True)
	main_id = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
	username= models.CharField(max_length=100)
	fname=models.CharField(max_length=100)
	lname= models.CharField(max_length=100)
	email= models. EmailField(max_length=254, unique=True)
	phone= models.TextField(default="0")
	country= models.TextField()
	birthday= models.TextField()
	joinedAt= models.DateField(default=date.today)

class Friends(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	friend_id = models.IntegerField()

class Currency(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	totalpts = models.IntegerField(default=0)

class Matches(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.TextField()
	players_A = models.CharField(max_length=100)
	players_B = models.CharField(max_length=100)
	result = ArrayField(models.TextField())
	game_timestamp = models.IntegerField(default=0)
	playedAt = models.DateField(default=date.today)


class FeaturedGames(models.Model):
	game = models.TextField()
	icon = models.URLField()
	bg = models.URLField()
	status = models.TextField()
	plat_form = models.TextField(default="None")

