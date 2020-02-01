# Discord Schedule Message Bot  [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
A Discord bot for scheduling and delaying user messages.
## Quickstart
1. Get Discord Bot token ([Instructions](https://www.writebots.com/discord-bot-token/))

1. Install:
    ```shell script
    pip install -r requirements.txt
    ```

1. Init:
    ```shell script
    python set_token.py %YOUR_DISCORD_APP_TOKEN%
    ```
   
1. Start RabbitMQ:

    This is subject to change due to security vulnerability
    ```shell script
    docker run -d -p 15672:15672 -p 5672:5672 --name some-lovely-name-for-rabbit rabbitmq:3
    ```

1. Start Celery worker:
    ```shell script
    python cli.py start_celery_worker
    ```

1. Start a server:
    ```shell script
    python cli.py start_server
    ```
