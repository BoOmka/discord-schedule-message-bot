import datetime as dt
import logging
import typing

import discord
from discord import TextChannel
from discord.ext import commands

import tasks

logger = logging.getLogger(__name__)
client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.group(aliases=['sd'])
async def scheduler(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@scheduler.command()
async def delay(ctx, channel: typing.Optional[TextChannel], countdown_minutes: int,  *, message: str):
    """Delays message for passed amount of minutes"""
    if channel is None:
        channel = ctx.message.channel

    countdown_td = dt.timedelta(minutes=countdown_minutes)
    tasks.send_message.apply_async(
        args=(channel.id, ctx.message.author.id, message),
        countdown=countdown_td.seconds,
    )
    await ctx.message.delete()


@scheduler.command(aliases=['yt'])
async def youtube(ctx,
                  channel: typing.Optional[TextChannel],
                  youtube_url: str,
                  resolution: typing.Optional[int] = 720,
                  comment: typing.Optional[str] = ''):
    """Schedules YT video until desired resolution becomes available"""
    if channel is None:
        channel = ctx.message.channel

    link = tasks.send_message.si(channel.id, ctx.message.author.id, comment) if comment else None
    tasks.send_message_yt.apply_async(
        args=(channel.id, ctx.message.author.id, youtube_url, resolution),
        link=link
    )

    await ctx.message.delete()


@bot.command()
async def ping(ctx):
    """Pings this bot"""
    await ctx.send('pong')


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} ({client.user.id})')
