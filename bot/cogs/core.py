from bot.utils.discord_util import paginate_embed
from discord.ext import commands
from bot.utils.help import GENSHIN_DATABASE_MD, GENSHIN_DISCORD_MINIGAME, REMINDERS_HELP, RESIN_STATUS
import discord

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="Genshin Impact"))

    @commands.command()
    async def help(self, ctx):
        embed1 = discord.Embed(title="Genshin Database", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red())
        embed2 = discord.Embed(title="Reminders", description=REMINDERS_HELP, color=discord.Colour.gold())
        embed3 = discord.Embed(title="Resin Status", description=RESIN_STATUS, color=discord.Colour.blue())
        embed4 = discord.Embed(title="Genshin Minigame", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green())
        await paginate_embed(self.bot, ctx, [embed1, embed2, embed3, embed4])