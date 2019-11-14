import asyncio
import datetime
import datetime as dt
import logging

import discord

import config
import models
from db import session

logger = logging.getLogger(__name__)
client = discord.Client()


async def schedule_message(
        channel_id: int,
        author_id: int,
        message: str,
        target_dt: dt.datetime,
        message_dbid: int = None,
):
    db_instance = models.ScheduledMessage(message=message, send_ts=target_dt)
    if message_dbid is not None:
        db_instance.id = message_dbid
    # TODO: https://github.com/BoOmka/discord-schedule-message-bot/issues/2
    # FIXME: doesn't save to DB for some reason
    session.add(db_instance)
    while dt.datetime.now() < target_dt:
        await asyncio.sleep(config.SCHEDULER_SLEEP_TIME)
    author = client.get_user(author_id)
    msg = f'**{author.mention} said:** {message}'
    await client.get_channel(channel_id).send(msg)


async def delay_message(channel_id: int, author_id: int, message: str, delay: float):
    target_dt = datetime.datetime.now() + dt.timedelta(minutes=delay)
    await schedule_message(channel_id, author_id, message, target_dt)


@client.event
async def on_message(message):
    _logger = logger.getChild('on_message')
    # don't respond to ourselves
    if message.author == client.user:
        return
    # ignore non-command messages
    if not message.content.startswith('!'):
        return

    if message.content.startswith('!help'):
        # TODO: https://github.com/BoOmka/discord-schedule-message-bot/issues/3
        await message.channel.send('Here goes short doc')
        return

    if message.content.startswith('!ping'):
        await message.channel.send('pong')
        return

    if message.content.startswith('!delay'):
        try:
            _, time, payload = message.content.split(' ', maxsplit=2)
            asyncio.ensure_future(delay_message(message.channel.id, message.author.id, payload, float(time)))
        except ValueError as e:
            _logger.exception(e)
        finally:
            await message.delete()
        return

    if message.content.startswith('!schedule'):
        # TODO: https://github.com/BoOmka/discord-schedule-message-bot/issues/1
        return


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} ({client.user.id})')
