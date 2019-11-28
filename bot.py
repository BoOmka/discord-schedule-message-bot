import datetime as dt
import logging

import discord

import models
import tasks
from db import session

logger = logging.getLogger(__name__)
client = discord.Client()


def delay_message(
        channel_id: int,
        author_id: int,
        message: str,
        countdown_minutes: float,
):
    countdown_td = dt.timedelta(minutes=countdown_minutes)
    target_dt = dt.datetime.utcnow() + countdown_td

    db_instance = models.ScheduledMessage(message=message,
                                          send_ts=target_dt,
                                          channel_id=channel_id,
                                          author_id=author_id)
    session.add(db_instance)
    session.commit()

    tasks.send_message.apply_async(
        args=(channel_id, author_id, message),
        countdown=countdown_td.seconds,
    )


def schedule_yt(
        channel_id: int,
        author_id: int,
        youtube_url: str,
        resolution: int,
):
    """

    :param channel_id: Channel from where
    :param author_id:
    :param youtube_url:
    :param resolution:
    :return:
    """
    db_instance = models.ScheduledVideo(video_url=youtube_url)
    session.add(db_instance)
    session.commit()


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

    if message.content.startswith('!delay '):
        try:
            _, countdown_minutes, payload = message.content.split(' ', maxsplit=2)
            delay_message(message.channel.id, message.author.id, payload, float(countdown_minutes))
        except ValueError as e:
            _logger.exception(e)
        else:
            await message.delete()
        return

    if message.content.startswith('!schedule '):
        # TODO: https://github.com/BoOmka/discord-schedule-message-bot/issues/1
        return

    if message.content.startswith('!scheduleyt'):
        try:
            _, url, resolution = message.content.split(' ', maxsplit=2)
            schedule_yt(message.channel.id,
                        message.author.id,
                        url,
                        resolution)
        except ValueError as e:
            _logger.exception(e)
        finally:
            await message.delete()
        return


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} ({client.user.id})')
