from sqlalchemy.sql.sqltypes import Boolean
from data.db import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'discordusers'
    id = Column(Integer, primary_key=True)
    reminders = relationship("Reminder", back_populates="owner")
    resin = relationship("Resin", uselist=False, back_populates="owner")
    profile = relationship("GameProfile", uselist=False, back_populates="owner")

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('discordusers.id'))
    owner = relationship("User", back_populates="reminders")
    when = Column(Date)
    channel = Column(String)
    message = Column(String)
    typing = Column(String)
    timezone = Column(String)

class Resin(Base):
    __tablename__ = 'resins'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('discordusers.id'))
    owner = relationship("User", back_populates="resin")
    timestamp = Column(Date)

class GameProfile(Base):
    __tablename__ = 'gameprofiles'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('discordusers.id'))
    owner = relationship("User", back_populates="profile")
    primogems = Column(Integer)
    characters = relationship("GameCharacter")
    stamina = Column(Integer)
    health = Column(Integer)
    level = Column(Integer)
    deathtime = Column(Date)

class GameCharacter(Base):
    __tablename__ = 'gamecharacters'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    profile_id = Column(Integer, ForeignKey('gameprofiles.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    constellation = Column(Integer)
    character = relationship("Character")
