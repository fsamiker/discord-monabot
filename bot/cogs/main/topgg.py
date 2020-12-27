import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import dbl

class Topgg(commands.Cog):
    def __init__(self, bot, dbl_token):
        self.bot = bot
        self.dbl_token = dbl_token
        self.dblpy = dbl.DBLClient(self.bot, self.dbl_token, autopost=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Connecting to topgg server...')

    async def on_guild_post():
        print("Server count posted successfully")
