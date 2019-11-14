import logging

import discord

logger = logging.getLogger(__name__)
client = discord.Client()


@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return
    # ignore non-command messages
    if not message.content.startswith('!'):
        return

    if message.content == '!ping':
        await message.channel.send('pong')


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} ({client.user.id})')
