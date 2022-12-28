from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db.models.signals import post_save
from django.dispatch import receiver

from bet.models import FeaturedGames, Users, Friends, Currency, Matches, FeaturedGames

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['username'] = user.username
		token['email'] = user.email
		return token


class GamesSerializer (serializers.ModelSerializer):
	class Meta:
		model = FeaturedGames
		fields =('game', 'icon', 'bg', 'status')



class UserRegisterSerializer (serializers.ModelSerializer):
	class Meta:
		model = User
		fields =('id','username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

	def create(validated_data):
		try:
			user = User.objects.create(
			username=validated_data['username'], 
			email=validated_data['email'], first_name=validated_data['first_name'], 
			last_name=validated_data['last_name'])
			user.set_password(validated_data['password'])
			user.save()
			return {'status':'Success', 'data':user}
		except:
			return {'status':'Error', 'data':'Cannot create the user'}



class MainUserSerializer (serializers.ModelSerializer):
	class Meta:
		model = Users
		fields=('main_id', 'username', 'fname', 'lname', 'email', 'phone', 'country', 'birthday', 'joinedAt')

	def get_user(id):
		req_user = Users.objects.get(main_id=id)
		userData = MainUserSerializer(req_user)
		return {'userData':userData.data}

	def createUser(newlyuser, validated_data):
		try:
			user_profile=Users.objects.create(
			main_id=newlyuser,
			username=validated_data['username'],
			fname=validated_data['first_name'],
			lname=validated_data['last_name'],
			email=validated_data['email'],
			phone=validated_data['phone'],
			country=validated_data['country'],
			birthday=validated_data['birthday'])
			user_profile.save()
			return {'status':'Success', 'data':'User has been created'} 
		except:
			return {'status':'Error', 'data':'Cannot create the user'}

class UsersSerializer (serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('main_id', 'username')

	def get_data(id):
		req_user = Users.objects.get(main_id=id)
		dataSer = UsersSerializer(req_user)
		return {'data':dataSer}


class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model=Currency
		fields={'user_id' ,'totalptl'}

	def createLog(newlyuser):
		insert_log=Currency.objects.create(user_id=newlyuser)
		insert_log.save()
		return {'status':'Success'}

	def updateLog(id):
		return id

