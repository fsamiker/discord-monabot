from discord import activity
from discord.ext import commands
import discord
from discord.ext.commands.cooldowns import BucketType

class Greetings(commands.Cog, name='Miscellaneous'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member