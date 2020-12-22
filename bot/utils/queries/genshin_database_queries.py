from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from data.genshin.models import Character, Food
from  sqlalchemy.sql.expression import func

def query_random_character(session):
    stmt = select(Character).order_by(func.random()).limit(1)
    char = session.execute(stmt).scalars().first()
    return char

def query_random_food(session):
    stmt = select(Food).order_by(func.random()).limit(1)
    food = session.execute(stmt).scalars().first()
    return food