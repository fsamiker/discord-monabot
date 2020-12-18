from discord.ext.commands.cooldowns import BucketType
from bot.utils.discord_util import paginate_embed, send_temp_embed
from discord.ext import commands
from bot.utils.help import GENSHIN_CANCELKREMINDERS, GENSHIN_CHECKREMINDERS, GENSHIN_DATABASE_MD, GENSHIN_DB_ARTIFACT, GENSHIN_DB_CHAR, GENSHIN_DB_CHAR_ASC, GENSHIN_DB_DOMAIN, GENSHIN_DB_ENEMY, GENSHIN_DB_FOOD, GENSHIN_DB_MATERIAL, GENSHIN_DB_TAL, GENSHIN_DB_TAL_MAT, GENSHIN_DB_WEAPON, GENSHIN_DB_WEAPON_MAT, GENSHIN_DISCORD_MINIGAME, GENSHIN_GAME_ATTACK, GENSHIN_GAME_CLAIM, GENSHIN_GAME_EXPLORE, GENSHIN_GAME_HEAL, GENSHIN_GAME_MUG, GENSHIN_GAME_PRIMOLVLUP, GENSHIN_GAME_PROFILE, GENSHIN_GAME_START, GENSHIN_GAME_SWITCH, GENSHIN_GAME_WEATHER, GENSHIN_GAME_WISH, GENSHIN_REMINDME, GENSHIN_RESIN_CHECK, GENSHIN_RESIN_SET, GENSHIN_RESIN_TIME, REMINDERS_HELP, RESIN_STATUS
import discord

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._help_dict = self.generate_help_embded_dict()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="Genshin Impact"))

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def help(self, ctx, *arg):
        category = ' '.join(arg)

        if category.lower() in self._help_dict.keys():
            await send_temp_embed(self.bot, ctx, self._help_dict[category])
            return
        if category.lower() == 'genshin database':
            embeds = []
            embeds.append(discord.Embed(title="Genshin Database - Commands", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red()))
            embeds.append(self._help_dict['character'])
            embeds.append(self._help_dict['character ascension'])
            embeds.append(self._help_dict['talent'])
            embeds.append(self._help_dict['talent material'])
            embeds.append(self._help_dict['weapon'])
            embeds.append(self._help_dict['weapon ascension'])
            embeds.append(self._help_dict['artifact'])
            embeds.append(self._help_dict['domain'])
            embeds.append(self._help_dict['material'])
            embeds.append(self._help_dict['food'])
            embeds.append(self._help_dict['enemy'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'reminders':
            embeds = []
            embeds.append(discord.Embed(title="Reminders - Commands", description=REMINDERS_HELP, color=discord.Colour.gold()))
            embeds.append(self._help_dict['remindme'])
            embeds.append(self._help_dict['checkreminders'])
            embeds.append(self._help_dict['cancelreminder'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'resin status':
            embeds = []
            embeds.append(discord.Embed(title="Resin Status - Commands", description=RESIN_STATUS, color=discord.Colour.blue()))
            embeds.append(self._help_dict['setresin'])
            embeds.append(self._help_dict['checkresin'])
            embeds.append(self._help_dict['timetoresin'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'genshin minigame':
            embeds = []
            embeds.append(discord.Embed(title="Geshin Minigame - Commands", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green()))
            embeds.append(self._help_dict['startadventure'])
            embeds.append(self._help_dict['claimdaily'])
            embeds.append(self._help_dict['profile'])
            embeds.append(self._help_dict['checkweather'])
            embeds.append(self._help_dict['primolvlup'])
            embeds.append(self._help_dict['switchactive'])
            embeds.append(self._help_dict['wish'])
            embeds.append(self._help_dict['explore'])
            embeds.append(self._help_dict['attack'])
            embeds.append(self._help_dict['heal'])
            embeds.append(self._help_dict['mug'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        else:
            embed1 = discord.Embed(title="Genshin Database", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red())
            embed2 = discord.Embed(title="Reminders", description=REMINDERS_HELP, color=discord.Colour.gold())
            embed3 = discord.Embed(title="Resin Status", description=RESIN_STATUS, color=discord.Colour.blue())
            embed4 = discord.Embed(title="Genshin Minigame", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green())
            await paginate_embed(self.bot, ctx, [embed1, embed2, embed3, embed4])
            
    def generate_help_embded_dict(self):
        return {
            'character': discord.Embed(title="Genshin Database - Character", description=GENSHIN_DB_CHAR, color=discord.Colour.dark_red()),
            'character ascension': discord.Embed(title="Genshin Database - Character Ascension", description=GENSHIN_DB_CHAR_ASC, color=discord.Colour.dark_red()),
            'talent': discord.Embed(title="Genshin Database - Talent", description=GENSHIN_DB_TAL, color=discord.Colour.dark_red()),
            'talent material': discord.Embed(title="Genshin Database - Talent Material", description=GENSHIN_DB_TAL_MAT, color=discord.Colour.dark_red()),
            'weapon': discord.Embed(title="Genshin Database - Weapon", description=GENSHIN_DB_WEAPON, color=discord.Colour.dark_red()),
            'weapon ascension': discord.Embed(title="Genshin Database - Weapon Ascension", description=GENSHIN_DB_WEAPON_MAT, color=discord.Colour.dark_red()),
            'artifact': discord.Embed(title="Genshin Database - Artifact", description=GENSHIN_DB_ARTIFACT, color=discord.Colour.dark_red()),
            'domain': discord.Embed(title="Genshin Database - Domain", description=GENSHIN_DB_DOMAIN, color=discord.Colour.dark_red()),
            'material': discord.Embed(title="Genshin Database - Material", description=GENSHIN_DB_MATERIAL, color=discord.Colour.dark_red()),
            'food': discord.Embed(title="Genshin Database - Food", description=GENSHIN_DB_FOOD, color=discord.Colour.dark_red()),
            'enemy': discord.Embed(title="Genshin Database - Enemy/Boss", description=GENSHIN_DB_ENEMY, color=discord.Colour.dark_red()),
            'remindme': discord.Embed(title="Reminders - Remindme", description=GENSHIN_REMINDME, color=discord.Colour.gold()),
            'checkreminders': discord.Embed(title="Reminders - Check", description=GENSHIN_CHECKREMINDERS, color=discord.Colour.gold()),
            'cancelreminder': discord.Embed(title="Reminders - Cancel", description=GENSHIN_CANCELKREMINDERS, color=discord.Colour.gold()),
            'startadventure': discord.Embed(title="Geshin Minigame - Start Adventure", description=GENSHIN_GAME_START, color=discord.Colour.green()),
            'claimdaily': discord.Embed(title="Geshin Minigame - Claim Daily", description=GENSHIN_GAME_CLAIM, color=discord.Colour.green()),
            'profile': discord.Embed(title="Geshin Minigame - Profile", description=GENSHIN_GAME_PROFILE, color=discord.Colour.green()),
            'checkweather': discord.Embed(title="Geshin Minigame - Check Weather", description=GENSHIN_GAME_WEATHER, color=discord.Colour.green()),
            'primolvlup': discord.Embed(title="Geshin Minigame - Primolvlup", description=GENSHIN_GAME_PRIMOLVLUP, color=discord.Colour.green()),
            'switchactive': discord.Embed(title="Geshin Minigame - Switch Character", description=GENSHIN_GAME_SWITCH, color=discord.Colour.green()),
            'wish': discord.Embed(title="Geshin Minigame - Wish", description=GENSHIN_GAME_WISH, color=discord.Colour.green()),
            'explore': discord.Embed(title="Geshin Minigame - Explore", description=GENSHIN_GAME_EXPLORE, color=discord.Colour.green()),
            'attack': discord.Embed(title="Geshin Minigame - Attack", description=GENSHIN_GAME_ATTACK, color=discord.Colour.green()),
            'heal': discord.Embed(title="Geshin Minigame - Heal", description=GENSHIN_GAME_HEAL, color=discord.Colour.green()),
            'mug': discord.Embed(title="Geshin Minigame - Mug", description=GENSHIN_GAME_MUG, color=discord.Colour.green()),
            'setresin': discord.Embed(title="Resin Status - Set", description=GENSHIN_RESIN_SET, color=discord.Colour.blue()),
            'checkresin': discord.Embed(title="Resin Status - Check", description=GENSHIN_RESIN_CHECK, color=discord.Colour.blue()),
            'timetoresin': discord.Embed(title="Resin Status - Time To Resin", description=GENSHIN_RESIN_TIME, color=discord.Colour.blue())
        }