from data.monabot.models import Update
from sqlalchemy.sql import select

def query_updates(session):
    stmt = select(Update).order_by(Update.timestamp.desc()).limit(5)
    updates = session.execute(stmt).scalars().all()
    return updates