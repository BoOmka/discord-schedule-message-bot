import click

import config
from bot import client as discord_client
from db import create_db_tables
from tasks import app
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


@cli.command()
def start_celery_worker():
    app.worker_main(argv=click.get_os_args())


if __name__ == '__main__':
    cli()
