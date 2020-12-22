from data.monabot.models import GameProfile
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from data.genshin.models import Character, Enemy, Food
from  sqlalchemy.sql.expression import func
from sqlalchemy import or_

def query_random_character(session):
    stmt = select(Character).order_by(func.random()).limit(1)
    char = session.execute(stmt).scalars().first()
    return char

def query_random_food(session):
    stmt = select(Food).order_by(func.random()).limit(1)
    food = session.execute(stmt).scalars().first()
    return food

def query_random_boss(session):
    stmt = select(Enemy).filter(or_(Enemy.typing=='Normal Boss', Enemy.typing=='Weekly Boss')).order_by(func.random()).limit(1)
    boss = session.execute(stmt).scalars().first()
    return boss

def query_total_players(session):
    stmt = select(func.sum(GameProfile.level))
    total = session.execute(stmt).scalars().first()
    return total
