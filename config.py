from decouple import config

LOG_LEVEL = config('LOG_LEVEL', default='DEBUG')
LOG_FILE_NAME = config('LOG_FILE_NAME', default='app.log')
LOGFILE_MAXSIZE_BYTES = config('LOGFILE_MAXSIZE_BYTES', cast=int, default=512*1024**2)  # 512 MiB

DISCORD_TOKEN = config('DISCORD_TOKEN')

DB_URI = config('DB_URI', default='sqlite:///dsmb.db')

SCHEDULER_SLEEP_TIME = config('SCHEDULER_SLEEP_TIME', cast=float, default=1.0)
