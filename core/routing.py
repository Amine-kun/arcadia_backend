from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/start-game/(?P<game_id>\w+)/$', consumers.PlayerConsumer.as_asgi()),
	re_path(r'ws/create-game/(?P<game_id>.*)/$', consumers.PartyConsumer.as_asgi()),
]