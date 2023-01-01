from django.shortcuts import render
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

import Q
from bet.models import FeaturedGames, Users, Friends
from bet.serializers import GamesSerializer, MainUserSerializer, UserRegisterSerializer, MyTokenObtainPairSerializer, CurrencySerializer, UsersSerializer

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
		q = Q(user_id_id = request.user.id) | Q(friend_id=request.user.id)
		getFriends = Friends.objects.friends(q)
		return Response({'response': 'you have got friends'}, status=status.HTTP_200_OK)

	elif request.method == 'POST':
		
	elif request.method == 'DELETE':
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
def getNotificationActor(request):
	if request.method == 'GET':
		actor_id = request.GET.get('pid')
		actor_Data = UsersSerializer.get_data(request.user.id)
		return Response(actor_Data, status=status.HTTP_200_OK)
	else :
		return Response({'response': 'wrong http req'}, status=status.HTTP_400_BAD_REQUEST)
	return Response({'response': 'something went wrong with sending the notif'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def RecordMatch(request):
	if request.method == 'POST':
		return Response({'detail':'match saved'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
