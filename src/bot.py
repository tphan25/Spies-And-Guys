import os
import discord
import urllib
from constants import RequestType
from actions import ACTIONS
from game_globals import LOBBY_LIST

DISCORD_WRITE_PRIVILEGES = 2048
CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_OAUTH_URL = 'https://discordapp.com/api/oauth2/authorize'

client = discord.Client()

@client.event
async def on_ready():
    query_string_configs = {'client_id': CLIENT_ID,
        'permissions': DISCORD_WRITE_PRIVILEGES,
        'scope': 'bot',
    }
    qs = urllib.parse.urlencode(query_string_configs)
    print('Please visit the following URL to invite your bot: {}'.format(
        DISCORD_OAUTH_URL + '?' + qs))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg_split = list(map(lambda s: s.strip(), message.content.split()))
    if len(msg_split) == 0:
        return
    if msg_split[0] == '!sg' and len(msg_split) > 1:
        action = ACTIONS.get(msg_split[1], None)
        if action:
            await action(message, msg_split)
            print(LOBBY_LIST)


token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
