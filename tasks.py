import asyncio
import datetime as dt

from celery import Celery
from pytube import YouTube
from sqlalchemy.orm.sync import update

import config
import models
from db import session
from utils import get_discord_client

app = Celery(main='messages', broker=config.CELERY_BROKER_URL, backend=config.CELERY_RESULT_BACKEND)


@app.task(name='celery_tasks.send_message')
def send_message(
        channel_id: int,
        author_id: int,
        message: str,
):
    async def _send_message(
            channel_id: int,
            author_id: int,
            message: str,
    ):
        async with get_discord_client() as client:
            client.get_channel(channel_id)
            db_instance = models.ScheduledMessage(message=message, send_ts=target_dt)
            session.add(db_instance)
            session.commit()
            session.close()
            author = client.get_user(author_id)
            msg = f'**{author.mention} said:** {message}'
            await client.get_channel(channel_id).send(msg)

    asyncio.run(_send_message(
        channel_id=channel_id,
        author_id=author_id,
        message=message,
    ))


@app.task(name='celery_tasks.send_message_yt')
def send_message_yt(
        channel_id: int,
        author_id: int,
        youtube_url: str,
        desired_resolution: int = 1080
):
    """Send message with YouTube url if it is of target quality or higher."""
    message = youtube_url
    streams = YouTube(youtube_url).streams.all()
    for stream in streams:
        if stream.resolution >= desired_resolution:
            target_dt = dt.datetime.utcnow()
            send_message.apply_async(
                args=(channel_id, author_id, message, target_dt),
            )


@app.task(name='celery_tasks.checkout_video_resolution')
def checkout_video_resolution(youtube_url: str):
    """
    Check available resolutions

    :param youtube_url: YouTube video URL
    :return resolutions: list of available resolutions
    """
    streams = YouTube(youtube_url).streams.all()
    resolutions = [stream.resolution for stream in streams]

    # save to db
    scheduled_video = session.query(models.ScheduledVideo).filter(models.ScheduledVideo.video_url == youtube_url)
    scheduled_video.resolutions = resolutions
    session.commit()
    return resolutions
