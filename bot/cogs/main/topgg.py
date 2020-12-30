from bot.utils.queries.minigame_queries import query_gameprofile
from data.monabot.models import Vote
from bot.utils.queries.vote_queries import query_vote
from datetime import datetime, timedelta
import discord
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy.ext.asyncio import AsyncSession
from discord.ext import commands
import dbl

class Topgg(commands.Cog):
    def __init__(self, bot, dbl_token):
        self.bot = bot
        self.voted = {}
        self.dbl_token = dbl_token
        self.dblpy = dbl.DBLClient(self.bot, self.dbl_token,
         webhook_path='/monadbl', webhook_auth='t3ZEQQoQRXgnWmxWEP4R', webhook_port=5000,
         autopost=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Connecting to topgg server...')

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        discord_id = 123123
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            voter = await s.run_sync(query_vote, discord_id=discord_id)
            if not voter:
                v = Vote(
                    discord_id=discord_id,
                    timestamp=datetime.utcnow()
                )
                s.add(v)
            else:
                voter.timestamp=datetime.utcnow()
            await s.commit()
        await self.reward_vote(discord_id)
        print(data)

    async def reward_vote(self, discord_id):
        user = self.bot.get_user(discord_id)
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            profile = await s.run_sync(query_gameprofile, discord_id=discord_id)
            if user is not None and profile:
                profile.primogems += 200
                try:
                    embed = discord.Embed(title='Thank You!', description=f'Thanks for the support!\n200 {self.bot.get_cog("Flair").get_emoji("Primogem")} added to minigame profile',
                    color=discord.Colour.purple())
                    await user.send(embed=embed)
                except:
                    print(f'Failed to send to user {user}')
                await s.commit()

    def get_duration(self, time):
        raw = time.total_seconds()
        hours = int(raw/3600)
        minutes = int(raw%3600)/60
        seconds = raw%60
        time_str = ''
        if hours:
            time_str += f'{hours} hr(s) '
        if minutes:
            time_str += f'{minutes} min(s)'
        if seconds:
            time_str += f'{seconds} sec(s)'
        return time_str

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def vote(self, ctx):
        """Vote for Mona"""

        embed = discord.Embed(title='Vote Mona', color=discord.Colour.purple())
        embed.set_thumbnail(url=self.bot.user.avatar_url, )
        embed.set_footer(text=f'@{ctx.author.name}')

        # check if user has voted
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            voter = await s.run_sync(query_vote, discord_id=ctx.author.id)
            now=datetime.utcnow()
            if voter is not None and voter.timestamp+timedelta(hours=12) < now:
                next_votetime = voter.timestamp+timedelta(hours=12)
                time_delta = next_votetime-datetime.utcnow()
                duration = self.get_duration(time_delta)
                embed.description = f'You have already voted for Mona\nThanks for the Support!\n\n**Next vote available in: {duration}**'
            else:
                embed.description = f"If you have enjoyed **Monabot**\nVote on [Topgg](https://top.gg/bot/781525788759031820/vote)\n\nRecieve 200 {self.bot.get_cog('Flair').get_emoji('Primogem')} for Mona's Minigame every 12 hours\nThanks for your support!"

        await ctx.send(embed=embed)