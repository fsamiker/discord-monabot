from datetime import datetime, time
from datetime import timedelta
from discord.ext import commands
import asyncio
import json
import pytz

class Reminder:
    
    def __init__(self, _id, ctx, when, message, owner, r_type, timezone='UTC'):
        self._id = _id
        self.ctx = ctx
        self.when = when
        self.message = message
        self.owner = owner
        self.r_type = r_type
        self.tz = timezone

    @property
    def display_name(self):
        return f'{self.r_type} - {self.get_display_time()} [#id:{self._id}]'

    def update_time(self, when):
        self.when = when

    def get_display_time(self):
        user_tz = pytz.timezone(self.tz)
        utc_tz = pytz.timezone('UTC')
        display_time = utc_tz.localize(self.when).astimezone(user_tz)
        return display_time.strftime("%d %b %Y, %H:%M %z")
    
    def clone(self):
        return Reminder(self._id, self.ctx, self.when, self.message, self.owner, self.r_type, self.tz)

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tz = self._load_timezones()
        self._reminder_list = []
        self._enable_reminders = True
        self.counter = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print('Starting Reminder Server...')
        loop = asyncio.get_event_loop()
        loop.create_task(self.reminder_processor())

    async def reminder_processor(self):
        while self._enable_reminders:
            now = datetime.utcnow()
            for i in range(len(self._reminder_list)):
                r = self._reminder_list[0]
                if r.when > now:
                    break
                await r.owner.send(r.message)
                self._reminder_list.pop(0)
            await asyncio.sleep(1)

    @commands.command()
    async def remindme(self, ctx, *args):
        """Sets reminder"""

        async def usage(message):
            examples = '''```Command: remindme <option> <values>         
Options: \u2022 resin - Max Resin reminder. Enter current resin value

Example Usage:
\u2022 $f remindme resin 50```'''
            await ctx.send(f'{message}\n{examples}')

        option = args[0].lower()

        if option not in ['resin']:
            await usage('Invalid option')
            return

        member_id = ctx.author.id

        if option == 'resin':
            resin_cog = self.bot.get_cog('Resin')
            if resin_cog is not None:

                if self.reminder_exists(ctx.author, 'Resin'):
                    await ctx.send(f'Resin Reminder already exists. You can adjust resin reminder with "setresin" command.')
                    return
                error = resin_cog.verify_resin(args[1])
                if error is not None:
                    await ctx.send(f'{error}')
                    return

                current_resin = int(args[1])
                resin_cog.set_current_resin(member_id, current_resin)
                current_time = datetime.utcnow()
                max_resin_time = resin_cog.get_max_resin_time(current_time, current_resin)
                timezone = self.timezone_convertor(ctx.guild.region.name)
                r = Reminder(self.counter, ctx, max_resin_time, f'<@{member_id}> your resin is full!', ctx.author, 'Resin', timezone)
                self.add_reminder(r)
                await ctx.send(f'Reminder set. {r.display_name}')
            else:
                await ctx.send('Resin reminder currently disabled')

    @commands.command()
    async def checkreminders(self, ctx):
        """Check current active reminders"""
        member = ctx.author

        active_reminders = [r.display_name for r in self.get_all_reminders(member)]
        if active_reminders:
            reminder_list = '\u2022 '+'\n\u2022 '.join(active_reminders)
            await member.send(f'```__Here is a list of your active reminders:__\n{reminder_list}```')
        else:
            await member.send(f'You do not seem to have any reminders set')

    @commands.command()
    async def cancelreminder(self, ctx, value):
        """Cancel a current reminder"""

        async def usage(message):
            examples = '''```Command: cancelreminder <reminder ID or all>         
Reminder ID: Reminder ID to be canceled. Get ID from checkreminders. Refer [#id<number>] in list
All: Cancels all users reminders

Example Usage:
\u2022 $f cancelreminder 5
\u2022 $f cancelreminder all```'''
            await ctx.send(f'{message}\n{examples}')

        if value.lower() == 'all':
            reminder_list = self.get_all_reminders(ctx.author)
            count = len(reminder_list)
            for r in reminder_list:
                _, index = self.get_reminder_by_id(r._id)
                self.delete_reminder(index)
            await ctx.send(f'{count} reminder(s) deleted')
            return

        try:
            _id = int(value)
        except:
            await usage(f'ID should be a number')
            return

        r, index = self.get_reminder_by_id(_id)
        
        if index is None:
            await ctx.send(f'Could not found reminder *#ID:{_id}*')
            return

        if r.owner != ctx.author:
            await ctx.send('You can only cancel your own reminders!')
            return

        self.delete_reminder(index)
        await ctx.send(f'Reminder #ID:{_id} has been cancelled')

    def _load_timezones(self):
        with open('data/utility/discord_timezones.json', 'r') as f:
            data = json.load(f)
        return data

    def add_reminder(self, reminder):
        self._reminder_list.append(reminder)
        self.sort_reminders()
        self.counter += 1

    def sort_reminders(self):
        self._reminder_list.sort(key=lambda r: r.when)

    def get_all_reminders(self, owner):
        return [r for r in self._reminder_list if r.owner == owner]

    def get_reminder_by_id(self, _id):
        for i, j in enumerate(self._reminder_list):
            if j._id == _id:
                index = i
                r = j
                break
        else:
            index = None
            r = None
        
        return r, index

    def delete_reminder(self, index):
        self._reminder_list.pop(index)

    def timezone_convertor(self, discord_region):
        if discord_region.lower() in self.tz.keys():
            return self.tz[discord_region]
        return 'UTC'

    def reminder_exists(self, owner, r_type):
        user_reminders = self.get_all_reminders(owner)
        duplicates = [r for r in user_reminders if r.r_type.lower() == r_type.lower()]
        return bool(duplicates)
