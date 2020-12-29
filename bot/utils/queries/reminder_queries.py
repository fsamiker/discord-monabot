from data.monabot.models import Reminder
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from  sqlalchemy.sql.expression import func


def query_next_reminder(session):
    stmt = select(Reminder).order_by(Reminder.when.asc())
    remind = session.execute(stmt).scalars().first()
    return remind

def query_reminder_by_id(session, _id):
    stmt = select(Reminder).filter_by(id=_id)
    remind = session.execute(stmt).scalars().first()
    return remind

def query_reminder_by_typing(session, discord_id, typing):
    stmt = select(Reminder).filter_by(discord_id=discord_id).filter(Reminder.typing.like(typing)).filter(~Reminder.typing.like(f'%Custom%'))
    remind = session.execute(stmt).scalars().first()
    return remind

def query_reminder_by_typing_all(session, discord_id, typing):
    stmt = select(Reminder).filter_by(discord_id=discord_id).filter(Reminder.typing.like(f'Custom%'))
    reminds = session.execute(stmt).scalars().all()
    return reminds

def query_all_reminders(session, discord_id):
    stmt = select(Reminder).filter_by(discord_id=discord_id)
    reminds = session.execute(stmt).scalars().all()
    return reminds