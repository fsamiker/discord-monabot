from data.monabot.models import Reminder, Resin
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from  sqlalchemy.sql.expression import func

def query_resin(session, discord_id):
    stmt = select(Resin).filter_by(discord_id=discord_id)
    resin = session.execute(stmt).scalars().first()
    return resin