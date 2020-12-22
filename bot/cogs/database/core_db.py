from discord.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine

class Query(commands.Cog):
    def __init__(self, bot, db_uri):
        self.bot = bot
        self.URI = db_uri
        self.engine = None

    @commands.Cog.listener()
    async def on_ready(self):
        engine = create_async_engine(self.URI, echo=True,)
        self.engine = engine
        print(f'Database connection ready!')