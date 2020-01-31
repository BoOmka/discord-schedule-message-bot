from decouple import config

LOG_LEVEL = config('LOG_LEVEL', default='DEBUG')
LOG_FILE_NAME = config('LOG_FILE_NAME', default='app.log')
LOGFILE_MAXSIZE_BYTES = config('LOGFILE_MAXSIZE_BYTES', cast=int, default=512*1024**2)  # 512 MiB

DISCORD_TOKEN = config('DISCORD_TOKEN')

SCHEDULER_SLEEP_TIME = config('SCHEDULER_SLEEP_TIME', cast=float, default=1.0)

RABBIT_USER = config('RABBIT_USER', default='guest')
RABBIT_PASSWORD = config('RABBIT_PASSWORD', default='guest')

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default=f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@localhost:5672/')
CELERY_ENABLE_UTC = False

YT_RETRY_COUNTDOWN = config('YT_RETRY_COUNTDOWN', default=60)  # seconds
YT_MAX_RETRIES = config('YT_MAX_RETRIES', default=60)  # times
