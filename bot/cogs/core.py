from bot.utils.discord_util import paginate_embed
from discord.ext import commands
from bot.utils.help import GENSHIN_CANCELKREMINDERS, GENSHIN_CHECKREMINDERS, GENSHIN_DATABASE_MD, GENSHIN_DB_ARTIFACT, GENSHIN_DB_CHAR, GENSHIN_DB_CHAR_ASC, GENSHIN_DB_DOMAIN, GENSHIN_DB_ENEMY, GENSHIN_DB_FOOD, GENSHIN_DB_MATERIAL, GENSHIN_DB_TAL, GENSHIN_DB_TAL_MAT, GENSHIN_DB_WEAPON, GENSHIN_DB_WEAPON_MAT, GENSHIN_DISCORD_MINIGAME, GENSHIN_GAME_ATTACK, GENSHIN_GAME_CLAIM, GENSHIN_GAME_EXPLORE, GENSHIN_GAME_HEAL, GENSHIN_GAME_MUG, GENSHIN_GAME_PRIMOLVLUP, GENSHIN_GAME_PROFILE, GENSHIN_GAME_START, GENSHIN_GAME_SWITCH, GENSHIN_GAME_WEATHER, GENSHIN_GAME_WISH, GENSHIN_REMINDME, GENSHIN_RESIN_CHECK, GENSHIN_RESIN_SET, GENSHIN_RESIN_TIME, REMINDERS_HELP, RESIN_STATUS
import discord

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="Genshin Impact"))

    @commands.command()
    async def help(self, ctx, *arg):
        category = ' '.join(arg)
        if category.lower() == 'genshin database':
            embeds = []
            embeds.append(discord.Embed(title="Genshin Database - Commands", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Character", description=GENSHIN_DB_CHAR, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Character Ascension", description=GENSHIN_DB_CHAR_ASC, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Talent", description=GENSHIN_DB_TAL, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Talent Material", description=GENSHIN_DB_TAL_MAT, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Weapon", description=GENSHIN_DB_WEAPON, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Weapon Ascension", description=GENSHIN_DB_WEAPON_MAT, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Artifact", description=GENSHIN_DB_ARTIFACT, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Domain", description=GENSHIN_DB_DOMAIN, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Material", description=GENSHIN_DB_MATERIAL, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Food", description=GENSHIN_DB_FOOD, color=discord.Colour.dark_red()))
            embeds.append(discord.Embed(title="Genshin Database - Enemy/Boss", description=GENSHIN_DB_ENEMY, color=discord.Colour.dark_red()))
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'reminders':
            embeds = []
            embeds.append(discord.Embed(title="Reminders - Commands", description=REMINDERS_HELP, color=discord.Colour.gold()))
            embeds.append(discord.Embed(title="Reminders - Remindme", description=GENSHIN_REMINDME, color=discord.Colour.gold()))
            embeds.append(discord.Embed(title="Reminders - Check", description=GENSHIN_CHECKREMINDERS, color=discord.Colour.gold()))
            embeds.append(discord.Embed(title="Reminders - Cancel", description=GENSHIN_CANCELKREMINDERS, color=discord.Colour.gold()))
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'resin status':
            embeds = []
            embeds.append(discord.Embed(title="Resin Status - Commands", description=RESIN_STATUS, color=discord.Colour.blue()))
            embeds.append(discord.Embed(title="Resin Status - Set", description=GENSHIN_RESIN_SET, color=discord.Colour.blue()))
            embeds.append(discord.Embed(title="Resin Status - Check", description=GENSHIN_RESIN_CHECK, color=discord.Colour.blue()))
            embeds.append(discord.Embed(title="Resin Status - Time To Resin", description=GENSHIN_RESIN_TIME, color=discord.Colour.blue()))
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'genshin minigame':
            embeds = []
            embeds.append(discord.Embed(title="Geshin Minigame - Commands", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Start Adventure", description=GENSHIN_GAME_START, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Claim Daily", description=GENSHIN_GAME_CLAIM, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Profile", description=GENSHIN_GAME_PROFILE, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Check Weather", description=GENSHIN_GAME_WEATHER, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Primolvlup", description=GENSHIN_GAME_PRIMOLVLUP, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Switch Character", description=GENSHIN_GAME_SWITCH, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Wish", description=GENSHIN_GAME_WISH, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Explore", description=GENSHIN_GAME_EXPLORE, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Attack", description=GENSHIN_GAME_ATTACK, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Heal", description=GENSHIN_GAME_HEAL, color=discord.Colour.green()))
            embeds.append(discord.Embed(title="Geshin Minigame - Mug", description=GENSHIN_GAME_MUG, color=discord.Colour.green()))
            await paginate_embed(self.bot, ctx, embeds)
            return
        else:
            embed1 = discord.Embed(title="Genshin Database", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red())
            embed2 = discord.Embed(title="Reminders", description=REMINDERS_HELP, color=discord.Colour.gold())
            embed3 = discord.Embed(title="Resin Status", description=RESIN_STATUS, color=discord.Colour.blue())
            embed4 = discord.Embed(title="Genshin Minigame", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green())
            await paginate_embed(self.bot, ctx, [embed1, embed2, embed3, embed4])