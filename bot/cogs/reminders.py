from datetime import datetime, time
from datetime import timedelta
from discord.ext import commands
import asyncio

class Reminder:
    
    def __init__(self, _id, ctx, when, message, owner, r_type):
        self._id = _id
        self.ctx = ctx
        self.when = when
        self.message = message
        self.owner = owner
        self.r_type = r_type
        self.when_str = when.strftime("%d %b %Y, %H:%M")

    @property
    def display_name(self):
        return f'{self.r_type} - {self.when_str} [#ID{self._id}]'

    def update_time(self, when):
        self.when = when
        self.when_str = when.strftime("%d %b %Y, %H:%M")

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._reminder_list = []
        self._enable_reminders = True
        self.counter = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print('Starting Reminder Server')
        loop = asyncio.get_event_loop()
        loop.create_task(self.reminder_processor())

    async def reminder_processor(self):
        while self._enable_reminders:
            now = datetime.now()
            for i in range(len(self._reminder_list)):
                r = self._reminder_list[0]
                if r.when > now:
                    break
                await r.owner.send(r.message)
                self._reminder_list.pop(0)
            await asyncio.sleep(1)

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


    @commands.command()
    async def remindme(self, ctx, *args):
        """Sets reminder. Options: [resin <value>]"""
        member_id = ctx.author.id

        if args[0].lower() == 'resin':
            resin_cog = self.bot.get_cog('Resin')
            if resin_cog is not None:
                error = resin_cog.verify_resin(args[1])
                if error is not None:
                    await ctx.send(f'{error}')
                    return
                current_resin = int(args[1])
                resin_cog.set_current_resin(member_id, current_resin)
                current_time = datetime.now()
                max_resin_time = resin_cog.get_max_resin_time(current_time, current_resin)
                r = Reminder(self.counter, ctx, max_resin_time, f'<@{member_id}> your resin is full!', ctx.author, 'Resin')
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
            await ctx.send(f'ID should be a number')
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