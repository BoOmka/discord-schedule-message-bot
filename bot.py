import datetime as dt
import logging

import discord
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
async def delay(ctx, countdown_minutes: int, *, message: str):
    """Delays message for passed amount of minutes"""
    countdown_td = dt.timedelta(minutes=countdown_minutes)
    tasks.send_message.apply_async(
        args=(ctx.message.channel.id, ctx.message.author.id, message),
        countdown=countdown_td.seconds,
    )


@scheduler.command(aliases=['yt'])
async def youtube(ctx, youtube_url: str, resolution: int):
    """Schedules YT video until desired resolution becomes available"""
    tasks.send_message_yt.apply_async(
        args=(ctx.message.channel.id, ctx.message.author.id, youtube_url, resolution))


@bot.command()
async def ping(ctx):
    """Pings this bot"""
    await ctx.send('pong')


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} ({client.user.id})')
