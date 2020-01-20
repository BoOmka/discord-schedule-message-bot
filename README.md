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
   
1. Start Redis:
    ```shell script
    docker run --name redis -p 6379:6379 -d redis:latest
    ```

    4.1. For Windows users: https://github.com/microsoftarchive/redis/releases
   
1. Start Celery worker:
    ```shell script
    python cli.py start-celery-worker
    ```

1. Start a server:
    ```shell script
    python cli.py start-server
    ```
