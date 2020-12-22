from data.monabot.models import GameCharacter, GameProfile
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from  sqlalchemy.sql.expression import func

def query_gameprofile(session, discord_id):
    stmt = select(GameProfile).\
        options(selectinload(GameProfile.characters).selectinload(GameCharacter.character)).\
            filter_by(discord_id=discord_id)
    user = session.execute(stmt).scalars().first()
    return user

def query_user_character(session, profile_id, character_id):
    stmt = select(GameCharacter).options(selectinload(GameCharacter.character)).filter_by(profile_id=profile_id, character_id=character_id)
    game_char = session.execute(stmt).scalars().first()
    return game_char

def query_user_active_character(session, profile_id):
    stmt = select(GameCharacter).options(selectinload(GameCharacter.character)).filter_by(active=True, profile_id=profile_id)
    char = session.execute(stmt).scalars().first()
    return char

def query_random_user_character(session, profile_id):
    stmt = select(GameCharacter).options(selectinload(GameCharacter.character)).filter_by(profile_id=profile_id).order_by(func.random())
    char = session.execute(stmt).scalars().first()
    return char 

def query_user_bench_characters(session, profile_id):
    stmt = select(GameCharacter).options(selectinload(GameCharacter.character)).filter_by(profile_id=profile_id,active=False)
    chars = session.execute(stmt).scalars().all()
    return chars