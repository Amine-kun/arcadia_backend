import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from bet.models import Lobby
from bet.serializers import LobbySerializer


class PlayerConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		print('connected')
		self.game_id = self.scope['url_route']['kwargs']['game_id']
		self.game_group_id = 'game_%s' % self.game_id

		await self.channel_layer.group_add(
			self.game_group_id,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		print('disconnected')
		await self.channel_layer.group_discard(
			self.game_group_id,
			self.channel_name
			)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)

		await self.channel_layer.group_send(
			self.game_group_id,
			{
				'type' : 'game_check',
				'user' : text_data_json["user"],
				'players' : text_data_json["players"],
				'playerData' : text_data_json["playerData"]
			}
			)

	async def game_check(self,event):
		user = event["user"]
		players = event["players"]
		playerData = event["playerData"]
		print(user)
		await self.send(text_data=json.dumps({
			'user' : user,
			'players' : players,
			'playerData' : playerData
			}))


@database_sync_to_async
def handleParty(id, user):
	checkIfExist = Lobby.objects.get(game_id = id)
	serializing = LobbySerializer(checkIfExist)

	if "id" in serializing.data:
		prev_data = checkIfExist.players
		isExists = False

		for item in prev_data:
			if "username" in item and item["username"] == user['username']:
				isExists = True
				break

		if isExists == False:
			prev_data.append({'id':user['main_id'],'username':user['username'],'profile_picture':user['profile_picture']})
			checkIfExist.players = prev_data
			checkIfExist.save()
			return 'player added'
		else:
			return 'player hasnt been added'

	else :
		return 'player hasne been added'


@database_sync_to_async
def handleCreation(id, user):
	try:
		create = Lobby.objects.create(
		game_id = id,
		status = 'inLobby',
		players =[{'id':user['main_id'],'username':user['username'], 'profile_picture':user['profile_picture']}]
		)
		create.save()
		return True
	except:
		return False

@database_sync_to_async
def getCurrentLobby(id):
	try:
		checkIfExist = Lobby.objects.get(game_id = id)
		serializing = LobbySerializer(checkIfExist)
		return serializing.data
	except:
		return 'There is no such game'


class PartyConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.party_id = self.scope['url_route']['kwargs']['game_id']
		self.party_group_id = 'party_%s' % self.party_id

		await self.channel_layer.group_add(
			self.party_group_id,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.party_group_id,
			self.channel_name
			)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		user = text_data_json["user"]
		print(text_data_json['status'])
		
		if text_data_json['status'] == 'creator':
			createParty = await handleCreation(self.party_id, user)
		else:
			checkForParty = await handleParty(self.party_id, user)
			print(checkForParty)

		getLobby = await getCurrentLobby(self.party_id)

		await self.channel_layer.group_send(
			self.party_group_id,
			{
				'type' : 'party_check',
				'data': getLobby
				
			}
			)

	async def party_check(self,event):
		getLobby = event["data"]

		await self.send(text_data=json.dumps({
			'players':getLobby
			}))


