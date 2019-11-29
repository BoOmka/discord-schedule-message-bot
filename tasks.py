import asyncio

from celery import Celery, group, chain
from pytube import YouTube

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
    asyncio.run(_send_message(
        channel_id=channel_id,
        author_id=author_id,
        message=message,
    ))


@app.task(bind=True, default_retry_delay=60, name='celery_tasks.send_message_yt')
def send_message_yt(self, channel_id: int, author_id: int, youtube_url: str, desired_resolution: int):
    """Send message with YouTube url if it is of target quality or higher."""
    # TODO Reuse _send_message code for both send_message and send_message_yt
    try:
        streams = YouTube(youtube_url).streams.all()
        resolutions = [parse_resolution(stream.resolution) for stream in streams]
        max_resolution = max(resolutions)
        assert max_resolution >= desired_resolution, "Resolution of {} is not acceptable to send yet".format(youtube_url)
        asyncio.run(_send_message(
            channel_id=channel_id,
            author_id=author_id,
            message=youtube_url,
        ))
    except Exception:
        # TODO Replace hardcoded constants with configurable values
        raise self.retry(countdown=60, max_retries=60*2)


def parse_resolution(resolution: str) -> int:
    """
    Convert NoneType or str to integer representation of resolution
    :param resolution: video resolution of str type, e.g. '1080p'
    :return resolution_int: integer representation of resolution
    """
    if not resolution:
        return 0
    else:
        resolution_int = int(resolution[:-1])
        return resolution_int


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
