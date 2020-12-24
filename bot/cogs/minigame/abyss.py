from discord.ext.commands.cooldowns import BucketType
from bot.utils.embeds import send_action_embed, send_game_embed_misc
from bot.utils.queries.minigame_queries import query_gameprofile
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
    HP_MULTIPLIER = 150

    def __init__(self, bot):
        self.bot = bot
        self._boss = None
        self._victors = None
        self._enable_abyss = True
        self._next_spawn_time = None
        self._abyss_icon = 'assets/genshin/icons/i_spiral_abyss.png'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Summoning the abyss...')
        self.bot.loop.create_task(self.abyss_summoner())


    async def abyss_summoner(self):
        while self._enable_abyss:
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                self._victors = None
                random_boss = await s.run_sync(query_random_boss)
                end = datetime.utcnow() + timedelta(seconds=self.BOSS_DURATION)
                self._next_spawn_time = datetime.utcnow() + timedelta(seconds=self.ABYSS_INTERVAL)
                if not random_boss:
                    pass
                else:
                    total_lvls = await s.run_sync(query_total_players)
                    max_hp = self.calculate_boss_maxhp(total_lvls)
                    self._boss = {
                        'hp': max_hp,
                        'max_hp': max_hp,
                        'name': random_boss.name,
                        'end': end,
                        'attackers': [],
                        'icon_url': random_boss.icon_url
                    }
            await asyncio.sleep(self.ABYSS_INTERVAL)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def checkabyss(self, ctx):
        """Check minigame abyss"""
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        now = datetime.now()
        flair = self.bot.get_cog("Flair")

        info_msg = 'Team up with you friends and try to defeat the boss.\n\u2022 The player that deals the killing blow will grant participants of their guild the winners pot!\n\u2022 Every other player that participated in taking down the boss will earn the consolation prize.'

        if self._boss["hp"] > 0 and self._boss["end"] > now:
            title = f'{self._boss["name"]} is terrorizing discord!'
        else:
            title = f'Discord Abyss'
        embed = discord.Embed(title=title, color=discord.Colour.purple())
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(
                name='Rewards Given',
                value=f'Slaying Guild: {flair.get_emoji("Primogem")} {self.WINNER_REWARD}, {flair.get_emoji("AR")} {self.WINNER_EXP} exp\nConsolation: {flair.get_emoji("Primogem")} {self.CONSOLATION}, {flair.get_emoji("AR")} {self.CONSOLATION_EXP} exp',
                inline=False)
        embed.add_field(
                name='Rules',
                value=info_msg,
                inline=False)
        if self._victors:
            win_msg = f'**Slayer:** {self._victors["name"]}\n**Guild:** {self._victors["guild"]}'
            when_display = self.convert_from_utc(self._victors["when"], server_region).strftime("%I:%M %p, %d %b %Y")
            embed.description = f'{self._boss["name"]} was slain at {when_display}!\n\n{win_msg}\n\nBut do not rest easy, something else seems to be approaching...\n'
            file = discord.File(self._abyss_icon, filename='image.png')
            spawn_time = self.convert_from_utc(self._next_spawn_time, server_region).strftime("%I:%M %p, %d %b %Y")
            embed.set_footer(text = f'Next boss spawning at: {spawn_time}')
        elif self._victors is None and self._boss['end'] < now:
            spawn_time = self.convert_from_utc(self._next_spawn_time, server_region).strftime("%I:%M %p, %d %b %Y")
            file = discord.File(self._abyss_icon, filename='image.png')
            embed.description = f'The abyss is currently empty.'
            embed.set_footer(text = f'Next boss spawning at: {spawn_time}')
        else:
            embed.description = f'Health {self._boss["hp"]}/{self._boss["max_hp"]}'
            file = discord.File(self._boss['icon_url'], filename='image.png')
            end_time = self.convert_from_utc(self._boss['end'], server_region).strftime("%I:%M %p, %d %b %Y")
            embed.set_footer(text = f'Abyss ends at: {end_time}')

        await ctx.send(embed=embed, file=file)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1,1,BucketType.user)
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def attackabyss(self, ctx):
        """Attack Abyss Boss"""

        cost = 15
        title=f'Entered the Abyss...'
        color=discord.Colour.purple()
        game_cog = self.bot.get_cog("Game")

        if self._victors is not None:
            await send_game_embed_misc(ctx, title, f'{self._boss["name"]} has already been slain..')
            return

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            user = await s.run_sync(query_gameprofile, discord_id=ctx.author.id)
            if not user:
                await game_cog.no_profile(ctx)
                return
            user = game_cog.check_user_status(user)
            if user.deathtime:
                await send_game_embed_misc(ctx, 'Invalid Action', f'You are currently respawning!')
                return
            if user.stamina < cost:
                await send_game_embed_misc(ctx, 'Invalid Action', f'Sorry you do not have enough stamina. Go take a nap and come back later')
                return
            user.stamina -= cost
            footer = f'Remaining Stamina: {user.stamina}/{user.max_stamina}'
            if ctx.author.id not in self._boss["attackers"]:
                self._boss["attackers"].append(ctx.author.id)
            # Calculate Damage
            crit = random.randint(0, 100)
            dmg = int(random.randint(50*user.level,user.level*game_cog.MAX_DMG_MULTIPLIER)*game_cog.bonus_rate(user))
            msg = ''
            if crit <= game_cog.CRIT_CHANCE:
                dmg = dmg*2
                msg += '\nA Critical Hit!'
            msg += f'\n{ctx.author.display_name} dealt {dmg} damage to {self._boss["name"]}!'
            self._boss["hp"] -= dmg
            if self._boss["hp"] <= 0:
                self._victors = {
                    'name': ctx.author.display_name,
                    'guild': ctx.guild.name,
                    'when': datetime.utcnow()
                }
                msg += f'\n\nYou have slain {self._boss["name"]}!\nGuild **{ctx.guild.name}** claims the spoils!'
                winning_members = [m.id for m in ctx.guild.members]
                await self.reward_boss_kill(s, winning_members)
            user = game_cog.check_user_status(user)
            await send_action_embed(ctx, title, msg.strip(), footer, color)
            await s.commit()

    async def reward_boss_kill(self, asyncsession, winning_members):
        for _id in self._boss["attackers"]:
            profile = await asyncsession.run_sync(query_gameprofile, discord_id=_id)
            if profile is None:
                continue
            if _id in winning_members:
                profile.primogems += self.WINNER_REWARD
                profile.exp += self.WINNER_EXP
            else:
                profile.primogems += self.CONSOLATION
                profile.exp += self.CONSOLATION_EXP
        
    def calculate_boss_maxhp(self, total_lvls):
        if total_lvls is None:
            total_lvls = 5
        lower_hp = int(total_lvls*self.HP_MULTIPLIER*3)
        higher_hp = int(total_lvls*self.HP_MULTIPLIER*6)
        n = random.randint(lower_hp, higher_hp)
        return n

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)
