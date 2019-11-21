import asyncio
import datetime as dt

from celery import Celery

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
        target_dt: dt.datetime,
):
    async def _send_message(
            channel_id: int,
            author_id: int,
            message: str,
            target_dt: dt.datetime,
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
        target_dt=target_dt,
    ))
