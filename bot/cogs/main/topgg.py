from datetime import datetime, timedelta
import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import dbl

class Topgg(commands.Cog):
    def __init__(self, bot, dbl_token):
        self.bot = bot
        self.voted = {}
        self.dbl_token = dbl_token
        self.dblpy = dbl.DBLClient(self.bot, self.dbl_token, autopost=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Connecting to topgg server...')

    async def on_guild_post():
        print("Server count posted successfully")

    def has_voted(self, discord_id):
        now = datetime.utcnow()
        if discord_id in self.voted.keys() and self.voted[discord_id] > now:
            return True
        else:
            return False

    def vote(self, discord_id):
        if self.has_voted(discord_id):
            return
        self.voted[discord_id] = datetime.utcnow()
        return True

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
    async def vote(self, ctx):
        """Claim Mona Vote Primogems"""

        embed = discord.Embed(title='Vote Mona', color=discord.Colour.purple())
        embed.set_thumbnail(url=self.bot.user.avatar_url, )
        embed.set_footer(text=f'@{ctx.author.name}')

        # check if user has voted

        if self.has_voted(ctx.author.id):
            next_votetime = self.voted[ctx.author.id]+timedelta(hours=12)
            time_delta = next_votetime-datetime.utcnow()
            duration = self.get_duration(time_delta)
            embed.description = f'You have already voted for Mona\nThanks for the Support!\n\n**Next vote available in: {duration}**'
        else:
            embed.description = f"If you have enjoyed **Monabot**\nVote on [Topgg](https://top.gg/bot/781525788759031820/vote)\n\nClaim 200 {self.bot.get_cog('Flair').get_emoji('Primogem')} for Mona's Minigame every 12 hours\nThanks for your support!"

        await ctx.send(embed=embed)