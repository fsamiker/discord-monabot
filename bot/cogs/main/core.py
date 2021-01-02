from bot.utils.queries.misc_queries import query_updates
from discord.ext.commands.cooldowns import BucketType
from bot.utils.embeds import paginate_embed, send_temp_embed
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.help import GENSHIN_ADVENTURE_INFO, GENSHIN_CANCEL_REMINDERS, GENSHIN_CHECKREMINDERS, GENSHIN_DATABASE_MD, GENSHIN_DB_ARTIFACT, GENSHIN_DB_CHAR, GENSHIN_DB_CHAR_ASC, GENSHIN_DB_DOMAIN, GENSHIN_DB_ENEMY, GENSHIN_DB_FOOD, GENSHIN_DB_MATERIAL, GENSHIN_DB_TAL, GENSHIN_DB_TAL_MAT, GENSHIN_DB_WEAPON, GENSHIN_DB_WEAPON_MAT, GENSHIN_DISCORD_MINIGAME, GENSHIN_GAME_ATTACK, GENSHIN_GAME_ATTACKABYSS, GENSHIN_GAME_CHECKABYSS, GENSHIN_GAME_CLAIM, GENSHIN_GAME_EXPLORE, GENSHIN_GAME_HEAL, GENSHIN_GAME_LEADERBOARDS, GENSHIN_GAME_MUG, GENSHIN_GAME_PRIMOLVLUP, GENSHIN_GAME_PROFILE, GENSHIN_GAME_START, GENSHIN_GAME_SWITCH, GENSHIN_GAME_WEATHER, GENSHIN_GAME_WISH, GENSHIN_GENERAL_MD, GENSHIN_GENERAL_MD_V2, GENSHIN_INVITE_MONA, GENSHIN_REMINDME, GENSHIN_RESIN_CHECK, GENSHIN_RESIN_SET, GENSHIN_RESIN_SPEND, GENSHIN_RESIN_TIME, GENSHIN_SUPPORT, GENSHIN_UPDATE, GENSHIN_VOTE_MONA, REMINDERS_HELP, RESIN_STATUS
import discord

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._help_dict = self.generate_help_embded_dict()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Game(name="m!help"))

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def updates(self, ctx):
        """Get recent monabot updates"""
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            updates = await s.run_sync(query_updates)
            if not updates:
                embed = discord.Embed(title='Monabot Updates', description='There does not seem to be any recent updates to retrieve')
                await ctx.send(embed=embed)
                return
            else:
                pages = []
                for change in updates:
                    change_date = self.convert_from_utc(change.timestamp, server_region).strftime("%d %b %Y")
                    embed = discord.Embed(title='Monabot Updates', description=f'**{change_date}**\n', color=discord.Colour.purple())
                    changes = change.get_changes()
                    for k, v in changes.items():
                        embed.add_field(name=k, value=v, inline=False)
                    pages.append(embed)

        await paginate_embed(self.bot, ctx, pages)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def support(self, ctx):
        """Get monabot support resource links"""

        desc = '\u2022 [Discord Support Server](https://discord.gg/mgvEPfzDEs)\u2022 [Top GG Page](https://top.gg/bot/781525788759031820)'
        embed = discord.Embed(title='Support Resource Links', description=desc, color=discord.Colour.purple())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def invitemona(self, ctx):
        """Get Mona invite link"""
        desc = 'Share the word that mona is on discord!\nYou can invite mona to other servers with the following link:\n[Invite Link](https://discord.com/api/oauth2/authorize?client_id=781525788759031820&permissions=519232&scope=bot)'
        embed = discord.Embed(title='Invite Mona', description=desc, color=discord.Colour.purple())
        embed.set_thumbnail(url=self.bot.user.avatar_url, )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def help(self, ctx, *arg):
        category = ' '.join(arg)

        if category.lower() in self._help_dict.keys():
            if isinstance(ctx.channel, discord.channel.DMChannel) or not ctx.message.channel.guild.me.permissions_in(ctx.channel).manage_messages:
                await ctx.send(embed=self._help_dict[category])
            else:
                await send_temp_embed(self.bot, ctx, self._help_dict[category])
            return

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=discord.Embed(title="Overview", description=GENSHIN_GENERAL_MD, color=discord.Colour.purple()))
            return
        if not ctx.message.channel.guild.me.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=discord.Embed(title="Overview", description=GENSHIN_GENERAL_MD_V2, color=discord.Colour.purple()))
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
            embeds.append(self._help_dict['spendresin'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        if category.lower() == 'genshin minigame':
            embeds = []
            embeds.append(discord.Embed(title="Geshin Minigame - Commands", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green()))
            embeds.append(self._help_dict['startadventure'])
            embeds.append(self._help_dict['adventureinfo'])
            embeds.append(self._help_dict['vote'])
            embeds.append(self._help_dict['leaderboard'])
            embeds.append(self._help_dict['claimdaily'])
            embeds.append(self._help_dict['profile'])
            embeds.append(self._help_dict['checkweather'])
            embeds.append(self._help_dict['checkabyss'])
            embeds.append(self._help_dict['primolvlup'])
            embeds.append(self._help_dict['switchactive'])
            embeds.append(self._help_dict['wish'])
            embeds.append(self._help_dict['explore'])
            embeds.append(self._help_dict['attack'])
            embeds.append(self._help_dict['heal'])
            embeds.append(self._help_dict['mug'])
            embeds.append(self._help_dict['attackabyss'])
            await paginate_embed(self.bot, ctx, embeds)
            return
        else:
            embed0 = discord.Embed(title="Overview", description=GENSHIN_GENERAL_MD, color=discord.Colour.purple())
            embed1 = discord.Embed(title="Genshin Database", description=GENSHIN_DATABASE_MD, color=discord.Colour.dark_red())
            embed2 = discord.Embed(title="Reminders", description=REMINDERS_HELP, color=discord.Colour.gold())
            embed3 = discord.Embed(title="Resin Status", description=RESIN_STATUS, color=discord.Colour.blue())
            embed4 = discord.Embed(title="Genshin Minigame", description=GENSHIN_DISCORD_MINIGAME, color=discord.Colour.green())
            await paginate_embed(self.bot, ctx, [embed0, embed1, embed2, embed3, embed4])
            
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
            'cancelreminder': discord.Embed(title="Reminders - Cancel", description=GENSHIN_CANCEL_REMINDERS, color=discord.Colour.gold()),
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
            'timetoresin': discord.Embed(title="Resin Status - Time To Resin", description=GENSHIN_RESIN_TIME, color=discord.Colour.blue()),
            'checkabyss': discord.Embed(title="Geshin Minigame - Check Abyss", description=GENSHIN_GAME_CHECKABYSS, color=discord.Colour.blue()),
            'attackabyss': discord.Embed(title="Geshin Minigame - Attack Abyss", description=GENSHIN_GAME_ATTACKABYSS, color=discord.Colour.green()),
            'adventureinfo': discord.Embed(title="Geshin Minigame - How To Play", description=GENSHIN_ADVENTURE_INFO, color=discord.Colour.green()),
            'leaderboard': discord.Embed(title="Geshin Minigame - Leaderboard", description=GENSHIN_GAME_LEADERBOARDS, color=discord.Colour.green()),
            'updates': discord.Embed(title="Monabot - Update Log", description=GENSHIN_UPDATE, color=discord.Colour.purple()),
            'support': discord.Embed(title="Monabot - Support", description=GENSHIN_SUPPORT, color=discord.Colour.purple()),
            'invitemona': discord.Embed(title="Monabot - Invite", description=GENSHIN_INVITE_MONA, color=discord.Colour.purple()),
            'vote': discord.Embed(title="Monabot - Vote", description=GENSHIN_VOTE_MONA, color=discord.Colour.green()),
            'spendresin': discord.Embed(title="Resin Status - Spend Resin", description=GENSHIN_RESIN_SPEND, color=discord.Colour.blue())

        }

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)