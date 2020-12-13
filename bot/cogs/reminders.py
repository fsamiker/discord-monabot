import discord
from data.monabot.models import Reminder, Resin
from data.db import session_scope
from datetime import datetime, timedelta
from discord.ext import commands
import asyncio
import json
import pytz

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tz = self._load_timezones()
        self._next_reminder = {}
        self._enable_reminders = True

    @commands.Cog.listener()
    async def on_ready(self):
        print('Warming up Reminder Server...')
        loop = asyncio.get_event_loop()
        loop.create_task(self.reminder_processor())

    async def reminder_processor(self):
        print('Reminder server started!')
        self._get_next_reminder()
        while self._enable_reminders:
            now = datetime.utcnow()
            if self._next_reminder is not None and self._next_reminder.get('when') < now:
                user = self.bot.get_user(self._next_reminder.get('discord_id'))
                await user.send(self._next_reminder.get('message'))
                self._delete_reminder(self._next_reminder.get('id'))
                self._get_next_reminder()
            await asyncio.sleep(1)

    def _get_next_reminder(self):
        with session_scope() as s:
            r = s.query(Reminder).order_by(Reminder.when.asc()).first()
            if r:
                self._next_reminder = r.to_dict()
            else:
                self._next_reminder = None
    
    def _delete_reminder(self, id):
        with session_scope() as s:
            r = s.query(Reminder).get(id)
            s.delete(r)

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

    @commands.command()
    async def remindme(self, ctx, *args):
        """Sets reminder"""

        async def usage(message):
            examples = '''```Command: remindme <option> <values>         
Options: \u2022 resin - Max Resin reminder. Value = current resin value
         \u2022 specialty - Local Specialty reminder
         \u2022 mineral - Mineral Mining reminder

Example Usage:
\u2022 m!remindme resin 50
\u2022 m!remindme specialty
\u2022 m!remindme mineral```'''
            await ctx.send(f'{message}\n{examples}')

        option = args[0].lower()
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        message = ''

        if option not in ['resin', 'specialty', 'mineral']:
            await usage('Invalid option')
            return

        # resin reminder
        if option == 'resin':
            # validate resin input
            if len(args) != 2:
                await usage('Invalid Command')
                return
            resin_cog = self.bot.get_cog('Resin')
            error = resin_cog.verify_resin(args[1])
            if error is not None:
                await ctx.send(f'{error}')
                return

            with session_scope() as s:
                resin_value = int(args[1])
                resin = s.query(Resin).filter_by(discord_id=ctx.author.id).first()
                now = datetime.utcnow()
                max_resin_time = resin_cog.get_max_resin_time(now, resin_value)
                display_time = self.convert_from_utc(max_resin_time, server_region).strftime("%I:%M %p, %d %b %Y")
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
                # Check existing reminder
                r = s.query(Reminder).filter_by(discord_id=ctx.author.id, typing='Max Resin').first()
                if r:
                    r.when = max_resin_time
                    r.timezone = server_region
                    r.channel = ctx.channel.id
                    message += f'Existing reminder found, updated to {display_time}'
                # Create new reminder
                else:
                    r = Reminder(
                        discord_id=ctx.author.id,
                        when=max_resin_time,
                        channel=ctx.channel.id,
                        message=f'Your {self.bot.get_cog("Flair").get_emoji("Resin")} resin is full!',
                        typing='Max Resin',
                        timezone=server_region
                    )
                    s.add(r)
                    message += f'Max Resin {self.bot.get_cog("Flair").get_emoji("Resin")} reminder set for {display_time}'

        if option in ['specialty', 'mineral']:
            # validate specialty input
            if len(args) != 1:
                await usage('Invalid Command')
                return
            if option == 'specialty':
                days=2
                typing = 'Local Specialty Respawn'
                r_msg = f'Your local specialties have respawned!'
            elif option == 'mineral':
                days=3
                typing = 'Mineral Respawn'
                r_msg = f'Your minerals have respawned!'
            with session_scope() as s:
                now = datetime.utcnow()+timedelta(days=days)
                display_time = self.convert_from_utc(now, server_region).strftime("%I:%M %p, %d %b %Y")
                # Check existing reminder
                r = s.query(Reminder).filter_by(discord_id=ctx.author.id, typing=typing).first()
                if r:
                    r.when = now
                    r.timezone = server_region
                    r.channel = ctx.channel.id
                    message += f'Existing reminder found, updated to {display_time}'
                # Create new reminder
                else:
                    r = Reminder(
                        discord_id=ctx.author.id,
                        when=now,
                        channel=ctx.channel.id,
                        message=r_msg,
                        typing=typing,
                        timezone=server_region
                    )
                    s.add(r)
                    message += f'{typing} reminder set for {display_time}'

        self._get_next_reminder()

        await ctx.send(message)

    @commands.command()
    async def checkreminders(self, ctx):
        """Check current active reminders"""

        # Prepare embed
        embed = discord.Embed(title=f"{ctx.author.display_name.capitalize()}'s Reminders")
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        with session_scope() as s:
            reminders = s.query(Reminder).filter_by(discord_id=ctx.author.id).all()
            if reminders:
                embed.description = 'Below is a list of your active reminders'
                embed.set_footer(text=f'*Times are in {server_region.capitalize()} timezone')
                for r in reminders:
                    display_time = self.convert_from_utc(r.when, server_region).strftime("%I:%M %p, %d %b %Y")
                    embed.add_field(name=f'{r.typing}', value=f'{display_time}\nID: {r.id}', inline=True)
            else:
                embed.description = 'No reminders found.\nYou can set reminders using m!remindme command'
        
        await ctx.author.send(embed=embed)

    @commands.command()
    async def cancelreminder(self, ctx, value):
        """Cancel a current reminder"""

        async def usage(message):
            examples = '''```Command: cancelreminder <reminder ID or all>         
Reminder ID: Reminder ID to be canceled. Get ID from checkreminders. Refer [#id<number>] in list
All: Cancels all users reminders

Example Usage:
\u2022 m!cancelreminder 5
\u2022 m!cancelreminder all```'''
            await ctx.send(f'{message}\n{examples}')

        if value.lower() == 'all':
            with session_scope() as s:
                s.query(Reminder).filter_by(discord_id=ctx.author.id).delete()
            await ctx.send('All your reminders have been cancelled')
            return

        try:
            _id = int(value)
        except:
            await usage(f'ID should be a number. Check reminder id with m!checkreminders')
            return
        
        with session_scope() as s:
            r = s.query(Reminder).get(_id)
            if r:
                if r.discord_id != ctx.author.id:
                    await ctx.send('You can only cancel your own reminders!')
                else:
                    s.delete(r)
                    await ctx.send(f'{r.typing} reminder id:{r.id} has been cancelled')
            else:
                await ctx.send(f'Could not find reminder id:{_id}')