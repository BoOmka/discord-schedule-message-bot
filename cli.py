import click

import config
from bot import client
from utils import bootstrap


@click.group()
def cli():
    bootstrap()


@cli.command()
def start_server():
    client.run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    cli()
