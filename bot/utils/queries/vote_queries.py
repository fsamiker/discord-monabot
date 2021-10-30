from data.monabot.models import Reminder, Resin, Vote
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from  sqlalchemy.sql.expression import func

def query_vote(session, discord_id):
    stmt = select(Vote).filter_by(discord_id=discord_id)
    v = session.execute(stmt).scalars().first()
    return v