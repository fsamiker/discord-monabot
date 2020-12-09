from bot.utils.users import mention_by_id
from discord.ext import commands
from datetime import datetime, timedelta
import discord
import random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._wished = {}

    @commands.command()
    async def wish(self, ctx):
        """Make a wish!"""
        now = datetime.utcnow()
        member_id = ctx.author.id

        if member_id in self._wished.keys() and now < self._wished[member_id]:
            await ctx.send(f'Sorry you have already wished today')
            return
        else:
            self._wished[member_id] = now+timedelta(days=15)

        info_cog = self.bot.get_cog('Character')
        rolls = info_cog.get_all_character_names()

        n = random.randint(0, len(rolls)-1)
        wished = rolls[n]
        file = f'assets/genshin/characters/i_{wished}.png'
        await ctx.send(f'{wished} joins your party!',file=discord.File(file))

    @commands.command()
    async def quotes(self, ctx):
        """Well known genshin quotes"""
        quotes = [
            'Theres no reason to not roll for Zhongli - Pinocchio 2020',
            "I don't want Keqing - Pinocchio 2020",
        ]

        n = random.randint(0, len(quotes)-1)
        quote = quotes[n]
        await ctx.send(f'```{quote}```')

    @commands.command()
    async def attack(self, ctx, target: discord.Member):
        """Attack a player!"""
        maximum_dmg = 20000
        skills = self.bot.get_cog('Character').skills
        random_sk = random.choice(list(skills.keys()))
        dmg = random.randint(1, maximum_dmg)
        await ctx.send(f'You attacked {mention_by_id(target.id)} with "{random_sk}" for {dmg} damage!')