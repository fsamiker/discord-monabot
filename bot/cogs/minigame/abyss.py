from datetime import datetime, timedelta
from bot.utils.queries.genshin_database_queries import query_random_boss, query_total_players
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import discord
import random

class Abyss(commands.Cog):

    ABYSS_INTERVAL = 345600  # seconds
    BOSS_DURATION = 259200  # seconds
    WINNER_REWARD = 2500
    WINNER_EXP = 500
    CONSOLATION = 800
    CONSOLATION_EXP = 250

    def __init__(self, bot):
        self.bot = bot
        self._boss = None
        self._victors = None
        self._enable_abyss = True
        self._next_spawn_time = None
        self._abyss_icon = 'assets/icons/i_spiral_abyss.png'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Summoning the abyss...')
        self.bot.loop.create_task()

    async def abyss_summoner(self):
        while self._enable_abyss:
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                self._victors = None
                random_boss = await s.run_sync(query_random_boss)
                end = datetime.utcnow() + timedelta(seconds=self.BOSS_DURATION)
                self._next_spawn_time = datetime.utcnow() + timedelta(seconds=self.ABYSS_INTERVAL)
                total_lvls = await s.run_sync(query_total_players)
                print(total_lvls)
                self._boss = {
                    'hp': '',
                    'max_hp': '',
                    'name': random_boss.name,
                    'end': end,
                    'attackers': [],
                    'icon_url': random_boss.icon_url
                }
            await asyncio.sleep(self.ABYSS_INTERVAL)

    @commands.command()
    async def checkabyss(self, ctx):
        """Check minigame abyss"""
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        now = datetime.now()
        flair = self.bot.get_cog("Flair")

        info_msg = '```Team up with you friends and try to defeat the boss.\nThe player that deals the killing blow will grant his guild the winners pot!\nEvery other player that participated in taking down the boss will earn the consolation prize.```'

        embed = discord.Embed(title='Discord Abyss', color=discord.Colour.purple())
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(
                name='Rewards Given',
                value=f'Slaying Guild: {flair.get_emoji("Primogem")} {self.WINNER_REWARD}, {flair.get_emoji("AR")} {self.WINNER_EXP} exp\nConsolation: {flair.get_emoji("Primogem")} {self.CONSOLATION}, {flair.get_emoji("AR")} {self.CONSOLATION_EXP} exp')
        if self._victors:
            win_msg = f'Slayer: {self._victors["name"]}\nGuild: {self._victors["guild"]}'
            embed.description = f'{self._boss["name"]} was slain at {self._victors["when"]}!\n{}\n\nBut do not rest easy, something else seems to be approaching...\n{info_msg}'
            file = discord.File(self._abyss_icon, filename='image.png')
            spawn_time = self.convert_from_utc(self._next_spawn_time, server_region).strftime("%I:%M %p, %d %b %Y")
            embed.set_footer(text = f'Next boss spawning at: {spawn_time}')
        elif self._victors is None and self._boss['end'] < now:
            spawn_time = self.convert_from_utc(self._next_spawn_time, server_region).strftime("%I:%M %p, %d %b %Y")
            file = discord.File(self._abyss_icon, filename='image.png')
            embed.description = f'The abyss is currently empty.\n\n{info_msg}'
            embed.set_footer(text = f'Next boss spawning at: {spawn_time}')
        else:
            embed.description = f'{} is terrorizing discord!\nHealth {self._boss["hp"]}/{self._boss["max_hp"]}\n\n{info_msg}'
            file = discord.File(self._boss['icon_url'], filename='image.png')
            end_time = self.convert_from_utc(self._boss['end'], server_region).strftime("%I:%M %p, %d %b %Y")
            embed.set_footer(text = f'Abyss ends at: {end_time}')

        await ctx.send(embed=embed, file=file)

    @commands.command()
    async def attackabyss(self, ctx):
        pass

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)


                
    
    
