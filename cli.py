import click

import config
from bot import client as discord_client
from db import create_db_tables
from utils import bootstrap


@click.group()
def cli():
    bootstrap()


@cli.command()
def start_server():
    discord_client.run(config.DISCORD_TOKEN)


@cli.command()
def init_db():
    create_db_tables()


if __name__ == '__main__':
    cli()
