# database.py

from sqlalchemy import create_engine, Column, Integer, Date, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True, index=True)
    username = Column(String)
    target_refusals = Column(Integer, default=0)  # Целевое количество отказов
    current_refusals = Column(Integer, default=0)  # Текущее количество отказов
    state = Column(String, default="SET_TARGET")  # Текущее состояние пользователя


class RefusalHistory(Base):
    __tablename__ = 'refusal_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today)
    refusals = Column(Integer, default=0)


def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
