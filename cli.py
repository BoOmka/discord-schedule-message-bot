import click

import config
from bot import bot as discord_client
from tasks import app
from utils import bootstrap


@click.group()
def cli():
    bootstrap()


@cli.command()
def start_server():
    discord_client.run(config.DISCORD_TOKEN)


@cli.command()
def start_celery_worker():
    app.worker_main(argv=click.get_os_args())


if __name__ == '__main__':
    cli()
