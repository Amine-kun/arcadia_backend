import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from bet.models import Users, Notifications


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


@database_sync_to_async
def get_user(user_id):
	try:
		return Users.objects.get(main_id=user_id);
	except:
		return AnonymousUser()

@database_sync_to_async
def create_notification(receive, message):
	create_one=Notification.objects.create(user_revoker=receive,
										    message=message)
	return create_one

class NotificationConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user_id = self.scope['url_route']['kwargs']['user_id']
		self.user_group_id = 'user_%s' % self.user_id

		await self.channel_layer.group_add(
			self.user_group_id,
			self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.user_group_id,
			self.channel_name
			)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)

		user_send_id = text_data_json["sender"]
		user_receive_id = text_data_json["receiver"]
		message = text_data_json["message"]

		user_to_get = await get_user(int(user_receive_id))
		print(user_to_get)
		# push_notification = await create_notification(user_to_get, message)

		await self.channel_layer.group_send(
			self.user_group_id,
			{
				'type' : 'user_check',
				'value' : json.dumps(text_data)
			}
			)
	async def user_check(self, event):
		await self.send(json.dumps({
			'data':event
			}))


