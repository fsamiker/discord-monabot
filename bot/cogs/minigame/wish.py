from discord.ext import commands
import discord
from discord.ext.commands.cooldowns import BucketType
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

class Wishes(commands.Cog):

    REFRESH_INTERVAL = 86400  # seconds
    CHAR_NO = 4

    def __init__(self, bot):
        self.bot = bot
        self.banner_chars = []
        self._next_banner = []
        self.enable_cycle = True

    @commands.Cog.listener()
    async def on_ready(self):
        print('Generating Wish Banner...')
        self.bot.loop.create_task(self.banner_cycler())

    async def banner_cycler(self):
        while self.enable_cycle:
            pass

            await asyncio.sleep(self.REFRESH_INTERVAL)
    
    @commands.command()
    async def checkbanner(self, ctx):
        """Check current minigame banner"""
        pass

    @commands.command()
    @commands.is_owner()
    async def set_next_banner(self, ctx, chars):
        """Admin command, set next banner"""
        characters = chars.split(" ")

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            pass

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)
