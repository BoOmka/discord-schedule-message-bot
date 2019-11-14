from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import metadata


def get_engine():
    return create_engine(config.DB_URI)


def create_db_tables():
    metadata.create_all(get_engine())


Session = sessionmaker(bind=get_engine())

session = Session()

if __name__ == '__main__':
    create_db_tables()
