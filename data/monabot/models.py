from enum import unique
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime
from data.db import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger)
    when = Column(DateTime)
    channel = Column(String)
    message = Column(String)
    typing = Column(String)
    timezone = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'discord_id': self.discord_id,
            'when': self.when,
            'channel': self.channel,
            'message': self.message,
            'typing': self.typing,
            'timezone': self.timezone
        }

    def __repr__(self):
        return f'<{self.discord_id} - {self.typing}>'

class Resin(Base):
    __tablename__ = 'resins'
    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    resin = Column(Integer)
    timestamp = Column(DateTime)

class GameProfile(Base):
    __tablename__ = 'gameprofiles'
    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    primogems = Column(Integer)
    characters = relationship("GameCharacter")
    stamina = Column(Integer)
    max_stamina = Column(Integer)
    health = Column(Integer)
    max_health = Column(Integer)
    level = Column(Integer)
    exp = Column(Integer)
    max_exp = Column(Integer)
    deathtime = Column(DateTime)
    pity = Column(Integer)
    last_check = Column(DateTime)
    last_claim = Column(DateTime)

class GameCharacter(Base):
    __tablename__ = 'gamecharacters'
    active = Column(Boolean)
    profile_id = Column(Integer, ForeignKey('gameprofiles.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    constellation = Column(Integer)
    character = relationship("Character", uselist=False)