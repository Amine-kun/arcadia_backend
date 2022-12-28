import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


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



class PartyConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		print('connected to party')
		self.party_id = self.scope['url_route']['kwargs']['game_id']
		self.party_group_id = 'party_%s' % self.party_id

		await self.channel_layer.group_add(
			self.party_group_id,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		print('disconnected')
		await self.channel_layer.group_discard(
			self.party_group_id,
			self.channel_name
			)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)

		await self.channel_layer.group_send(
			self.party_group_id,
			{
				'type' : 'party_check',
				'user': text_data_json["user"]
				
			}
			)

	async def party_check(self,event):
		user = event["user"]

		await self.send(text_data=json.dumps({
			'user':user
			}))


