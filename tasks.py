import asyncio
import datetime as dt
import time

from celery import Celery
from pytube import YouTube

import config
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
    async def _wait_for_yt(
            channel_id: int,
            author_id: int,
            youtube_url: str,
            desired_resolution: int = 1080
    ):
        """Delay message with YT url until video gets processed to desired resolution."""
        message = youtube_url
        while True:
            streams = YouTube(youtube_url).streams.all()
            for stream in streams:
                if stream.resolution >= desired_resolution:
                    target_dt = dt.datetime.utcnow()
                    await send_message(channel_id, author_id, message, target_dt)
                    return
            await asyncio.sleep(config.SCHEDULER_SLEEP_TIME)
            # TODO: add timeout for videos which never reach target quality

    asyncio.run(_wait_for_yt(
        channel_id=channel_id,
        author_id=author_id,
        youtube_url=youtube_url,
        desired_resolution=desired_resolution,
    ))


@app.task(name='celery_tasks.send_message_yt')
def send_message_yt(
        channel_id: int,
        author_id: int,
        youtube_url: str,
        desired_resolution: int = 1080
):
    async def _wait_for_yt(
            channel_id: int,
            author_id: int,
            youtube_url: str,
            desired_resolution: int = 1080
    ):
        """Delay message with YT url until video gets processed to desired resolution."""
        message = youtube_url
        while True:
            streams = YouTube(youtube_url).streams.all()
            for stream in streams:
                if stream.resolution >= desired_resolution:
                    target_dt = dt.datetime.utcnow()
                    await send_message(channel_id, author_id, message, target_dt)
                    return
            await asyncio.sleep(config.SCHEDULER_SLEEP_TIME)
            # TODO: add timeout for videos which never reach target quality

    asyncio.run(_wait_for_yt(
        channel_id=channel_id,
        author_id=author_id,
        youtube_url=youtube_url,
        desired_resolution=desired_resolution,
    ))
