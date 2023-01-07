from django.shortcuts import render
from django.db.models import Q
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from bet.models import FeaturedGames, Users, Friends
from bet.serializers import FriendsSerializer, GamesSerializer, MainUserSerializer, UserRegisterSerializer, MyTokenObtainPairSerializer, CurrencySerializer, UsersSerializer

# App views fns

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

		
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
	if request.method == 'POST':
		user_data = JSONParser().parse(request)
		UserSerializer = UserRegisterSerializer.create(validated_data = user_data)

		if UserSerializer["status"] == 'Success':
			UserProfile = MainUserSerializer.createUser(newlyuser=UserSerializer['data'], validated_data=user_data)
			setCurrencyLog = CurrencySerializer.createLog(newlyuser=UserSerializer['data'])
			return Response({'data':UserProfile['data']}, status=status.HTTP_200_OK)			
		else:
			return Response({'ErrorDetails':UserSerializer['data']}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def getOnGamesView(request):
	if request.method == 'GET':
		games = FeaturedGames.objects.all()
		games_sers = GamesSerializer(games, many=True)
		return JsonResponse(games_sers.data, safe=False)
	return JsonResponse('bad response', safe=False)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def currentUser(request):
	if request.method == 'GET':
		getUser = MainUserSerializer.get_user(request.user.id)
		return Response(getUser, status=status.HTTP_200_OK)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def friends(request):
	if request.method == 'GET':
		you = MainUserSerializer.get_user(request.user.id)
		getFriends = Friends.objects.filter(user_id=request.user.id)
		friendsObj=[]

		for friend in getFriends:
			friendData=MainUserSerializer.get_user(friend.friend_id)
			friendsObj.append({'id':friendData['userData']['main_id'],'username':friendData['userData']['username'],'profile_picture':friendData['userData']['profile_picture']})

		return Response({'data':friendsObj}, status=status.HTTP_200_OK)

	elif request.method == 'POST':
		friendId = JSONParser().parse(request)
		friend = User.objects.get(id=friendId['id'])
		addFriendToYou= Friends.objects.create(user_id=request.user.id, friend_id=friend.id)
		addFriendToYou.save()

		addYouToFriend = Friends.objects.create(user_id=friend.id, friend_id=request.user.id)
		addYouToFriend.save()

		return Response({'details':'friend request has been accepted'}, status=status.HTTP_200_OK)

	elif request.method == 'DELETE':
		friendToDelete = request.DELETE.get('uid')
		deleteFriend = Friends.objects.get(friend_id=friendToDelete)
		dependencies.delete()
		return Response({'delete':'You unfriended a friend'})

	else:
		return Response({'response': 'wrong http req'}, status=status.HTTP_400_BAD_REQUEST)
	return Response({'response': 'something went wrong with sending the notif'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Notifications(request):
    if request.method == 'POST':
    	notify_data = JSONParser().parse(request)
    	sender = User.objects.get(id=request.user.id)
    	receiver = User.objects.get(id=notify_data['receiver_id'])
    	verb = notify_data['verb']
    	message = notify_data['message']
    	notify.send(sender, recipient=receiver, verb=verb, description=message)
    	return Response({'response': 'notif has been sent'}, status=status.HTTP_200_OK)
    else:
        return Response({'response': 'wrong http req'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'response': 'something went wrong with sending the notif'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActor(request):
	if request.method == 'GET':
		user_id = request.GET.get('uid')
		user_data = MainUserSerializer.get_user(user_id)
		data = user_data['userData']
		return Response({'id':data['main_id'], 'username':data['username'], 'profile_picture':data['profile_picture'], 'bio':data['bio']}, status=status.HTTP_200_OK)
	else :
		return Response({'response': 'wrong http req'}, status=status.HTTP_400_BAD_REQUEST)
	return Response({'response': 'something went wrong with sending the notif'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Search(request):
	if request.method == 'GET':
		user_id = request.GET.get('q')
		query = user_id.lower()
		data = Users.objects.filter(username__icontains=query)
		users=[]
		for result in data:
			users.append({'id':result.main_id,'username':result.username,'profile_picture':result.profile_picture})
		return Response({'data':users}, status=status.HTTP_200_OK)
	else :
		return Response({'response': 'wrong http req'}, status=status.HTTP_400_BAD_REQUEST)
	return Response({'response': 'something went wrong with sending the notif'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def RecordMatch(request):
	if request.method == 'POST':
		return Response({'detail':'match saved'}, status=status.HTTP_200_OK)
