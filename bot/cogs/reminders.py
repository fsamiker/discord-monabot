from bot.utils.help import TIMEZONE_NOTICE
from discord.ext.commands.errors import UserInputError
from bot.utils.queries.resin_queries import query_resin
from bot.utils.queries.reminder_queries import query_all_reminders, query_next_reminder, query_reminder_by_id, query_reminder_by_typing, query_reminder_by_typing_all
import discord
from discord.ext.commands.cooldowns import BucketType
from data.monabot.models import Reminder, Resin
from datetime import datetime, timedelta
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import json
import pytz
import re

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tz = self._load_timezones()
        self._next_reminder = {}
        self._enable_reminders = True
        self.duration_regex = re.compile(r'((?P<days>\d+?)d)?((?P<hours>\d+?)hr)?((?P<minutes>\d+?)min)?((?P<seconds>\d+?)sec)?')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Warming up Reminder Server...')
        loop = asyncio.get_event_loop()
        loop.create_task(self.reminder_processor())

    async def reminder_processor(self):
        print('Reminder server started!')
        await self._get_next_reminder()
        while self._enable_reminders:
            now = datetime.utcnow()
            if self._next_reminder is not None and self._next_reminder.get('when') < now:
                user = self.bot.get_user(self._next_reminder.get('discord_id'))
                if user is not None:
                    try:
                        await user.send(self._next_reminder.get('message'))
                    except Exception:
                        print(f'Failed to send reminder to {user}')
                else:
                    print(f'Failed to find user {self._next_reminder.get("discord_id")}')
                await self._delete_reminder(self._next_reminder.get('id'))
                await self._get_next_reminder()
            await asyncio.sleep(1)

    async def _get_next_reminder(self):
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            r = await s.run_sync(query_next_reminder)
            if r:
                self._next_reminder = r.to_dict()
            else:
                self._next_reminder = None
    
    async def _delete_reminder(self, id):
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            r = await s.run_sync(query_reminder_by_id, _id=id)
            s.delete(r)
            await s.commit()

    def _load_timezones(self):
        with open('data/utility/discord_timezones.json', 'r') as f:
            data = json.load(f)
        return data

    def timezone_convertor(self, discord_region):
        if discord_region.lower() in self.tz.keys():
            return self.tz[discord_region]
        return 'UTC'

    def convert_from_utc(self, time, server_region):
        user_tz = pytz.timezone(self.timezone_convertor(server_region))
        utc_tz = pytz.timezone('UTC')
        return utc_tz.localize(time).astimezone(user_tz)

    def parse_duration(self, time_str):
        parts = self.duration_regex.match(time_str)
        if not parts:
            return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def remindme(self, ctx, *args):
        """Sets reminder"""

        if not args:
            raise commands.UserInputError

        option = args[0].lower()
        flair = self.bot.get_cog("Flair")
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        message = ''

        if option not in ['resin', 'specialty', 'mineral', 'artifact', 'wei', 'custom']:
            raise UserInputError

        # resin reminder
        if option == 'resin':
            # validate resin input
            if len(args) < 2 or len(args) > 3:
                raise UserInputError
            resin_cog = self.bot.get_cog('Resin')
            resin_cog.verify_resin(args[1])
            resin_value = int(args[1])
            if len(args) == 3:
                resin_cog.verify_resin(args[2])
                target_resin = int(args[2])
            else:
                target_resin = 160
            if target_resin <= resin_value:
                raise UserInputError
            

            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                resin = await s.run_sync(query_resin, discord_id=ctx.author.id)
                now = datetime.utcnow()
                # Check existing resin entry
                if resin:
                    resin.resin=resin_value
                    resin.timestamp=now
                # Create new resin entry
                else:
                    resin = Resin(
                        discord_id=ctx.author.id,
                        resin=resin_value,
                        timestamp=now
                    )
                    s.add(resin)
                resin_time = resin_cog.get_resin_time(resin.timestamp, resin.resin, target_resin)
                target_display_time = self.convert_from_utc(resin_time, server_region).strftime("%I:%M %p, %d %b %Y")
                # Check existing reminder
                r = await s.run_sync(query_reminder_by_typing, discord_id=ctx.author.id, typing=f'Resin%')
                if r:
                    r.when = resin_time
                    r.timezone = server_region
                    r.channel = str(ctx.channel.id)
                    r.message = f'Your {flair.get_emoji("Resin")} resin has reached {target_resin}!'
                    r.value = str(target_resin)
                    message += f'Existing reminder found. Updated to {target_display_time}, Resin Threshold: {flair.get_emoji("Resin")} {target_resin}'
                # Create new reminder
                else:
                    r = Reminder(
                        discord_id=ctx.author.id,
                        when=resin_time,
                        channel=str(ctx.channel.id),
                        message=f'Your {flair.get_emoji("Resin")} resin has reached {target_resin}!',
                        typing=f'Resin {target_resin}',
                        timezone=server_region,
                        value=str(target_resin)
                    )
                    s.add(r)
                    message += f'{flair.get_emoji("Reminder")} Resin {target_resin} {flair.get_emoji("Resin")} -> {target_display_time}'
                await s.commit()

        if option in ['specialty', 'mineral', 'artifact', 'wei']:
            # validate specialty input
            if len(args) != 1:
                raise UserInputError
            if option == 'specialty':
                days=2
                typing = 'Local Specialty Respawn'
                r_msg = f'Your local specialties have respawned!'
            elif option == 'mineral':
                days=3
                typing = 'Mineral Respawn'
                r_msg = f'Your minerals have respawned!'
            elif option == 'artifact':
                days=1
                typing = 'Artifact Run Respawn'
                r_msg = f'Your Artifact Run has respawned!'
            elif option == 'wei':
                days=0.5
                typing = 'Wei Respawn'
                r_msg = f'Your Wei has respawned!'
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                now = datetime.utcnow()+timedelta(days=days)
                display_time = self.convert_from_utc(now, server_region).strftime("%I:%M %p, %d %b %Y")
                # Check existing reminder
                r = await s.run_sync(query_reminder_by_typing, discord_id=ctx.author.id, typing=typing)
                if r:
                    r.when = now
                    r.timezone = server_region
                    r.channel = str(ctx.channel.id)
                    message += f'Existing reminder found, updated to {display_time}'
                # Create new reminder
                else:
                    r = Reminder(
                        discord_id=ctx.author.id,
                        when=now,
                        channel=str(ctx.channel.id),
                        message=r_msg,
                        typing=typing,
                        timezone=server_region
                    )
                    s.add(r)
                    message += f'{flair.get_emoji("Reminder")} {typing} -> {display_time}'
                await s.commit()

        if option == 'custom':
            #Validate custom input
            if len(args) < 3:
                raise UserInputError
            r_msg = ' '.join(args[2:])
            when = self.parse_duration(args[1])
            if when is None or when > timedelta(days=60):
                raise UserInputError
            now = datetime.utcnow()+when
            display_time = self.convert_from_utc(now, server_region).strftime("%I:%M %p, %d %b %Y")
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            # Check existing reminder
                r = await s.run_sync(query_reminder_by_typing_all, discord_id=ctx.author.id, typing='Custom')
                if r and len(r) >= 3:
                    message += 'Maximum of 3 Custom Reminders already reached. Run `m!cancelreminder` to delete one before setting a new one.'
                else:
                    if len(r_msg) > 10:
                        typing = f'Custom "{r_msg[:10]}..."'
                    else:
                        typing = f'Custom "{r_msg}"'

                    r = Reminder(
                        discord_id=ctx.author.id,
                        when=now,
                        channel=str(ctx.channel.id),
                        message=f'Customer Reminder: {r_msg}',
                        typing=typing,
                        timezone=server_region
                    )
                    s.add(r)
                    message += f'{flair.get_emoji("Reminder")} Custom Reminder "{r_msg}" -> {display_time}'
                await s.commit()

        await self._get_next_reminder()

        if isinstance(ctx.channel, discord.channel.DMChannel):
            message += TIMEZONE_NOTICE
        await ctx.send(message)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def checkreminders(self, ctx):
        """Check current active reminders"""

        # Prepare embed
        embed = discord.Embed(title=f"{ctx.author.display_name.capitalize()}'s Reminders", color=discord.Colour.lighter_grey())
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            reminders = await s.run_sync(query_all_reminders, discord_id=ctx.author.id)
            if reminders:
                embed.description = 'Below is a list of your active reminders'
                if isinstance(ctx.channel, discord.channel.DMChannel):
                    embed.description += TIMEZONE_NOTICE
                embed.set_footer(text=f'*Times are in {server_region.capitalize()} timezone')
                for r in reminders:
                    display_time = self.convert_from_utc(r.when, server_region).strftime("%I:%M %p, %d %b %Y")
                    embed.add_field(name=f'{r.typing}', value=f'{display_time}\nID: {r.id}', inline=True)
            else:
                embed.description = 'No reminders found.\nYou can set reminders using `m!remindme` command'
        
        await ctx.author.send(embed=embed)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def cancelreminder(self, ctx, value):
        """Cancel a current reminder"""

        if value.lower() == 'all':
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                r = await s.run_sync(query_all_reminders, discord_id=ctx.author.id)
                for _ in r:
                    s.delete(_)
                await s.commit()
            await ctx.send('All your reminders have been cancelled')
            await self._get_next_reminder()
            return

        try:
            _id = int(value)
        except:
            raise UserInputError
        
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            r = await s.run_sync(query_reminder_by_id, _id=_id)
            if r:
                if r.discord_id != ctx.author.id:
                    await ctx.send('You can only cancel your own reminders!')
                    return
                else:
                    s.delete(r)
                    await s.commit()
                    await ctx.send(f'{r.typing} reminder ID:{r.id} has been cancelled')
            else:
                await ctx.send(f'Could not find reminder ID:{_id}')

        await self._get_next_reminder()
