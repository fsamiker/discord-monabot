from data import Base
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime
from sqlalchemy import Column, Integer, String
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
    value = Column(String)

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

class Update(Base):
    __tablename__ = 'updates'
    id = Column(Integer, primary_key=True)
    update_str = Column(String)
    timestamp = Column(DateTime)

    def update_list(self):
        return self.update_str.split(',')

    def get_changes(self):
        update_lst = self.update_str.split('###')
        i = 0
        updates = {}
        while i < len(update_lst):
            updates[update_lst[i]] = update_lst[i+1]
            i += 2
        return updates

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
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