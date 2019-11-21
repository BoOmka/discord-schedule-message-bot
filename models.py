from sqlalchemy import Column, Integer, MetaData, TEXT, Boolean, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class ScheduledMessage(Base):
    __tablename__ = 'scheduled_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(TEXT, nullable=False)
    send_ts = Column(TIMESTAMP, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    __table_args__ = (Index('scheduled_messages_is_sent_idx', 'is_sent'),)


class ScheduledVideos(Base):
    __tablename__ = 'scheduled_videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_url = Column(TEXT, nullable=False)
    send_ts = Column(TIMESTAMP, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    __table_args__ = (Index('scheduled_videos_is_sent_idx', 'is_sent'),)
