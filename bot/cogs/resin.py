import discord
from datetime import datetime, timedelta
from discord.ext import commands

class Resin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.max_resin = 160
        self.resin_rate = 8  #minutes
        self._resin_list = {}

    @commands.command()
    async def currentresin(self, ctx, *, member: discord.Member=None):
        """Shows current resin value. Blank for self or Tag a user"""
        if member is None:
            member = ctx.message.author
        member_id = member.id
        member_name = member.display_name
        if member_id in self._resin_list.keys():
            resin_details = self._resin_list[member_id]
            time = resin_details['time']
            set_resin = resin_details['resin']
            resin_added = (datetime.now() - time).seconds/(8*60)
            if (set_resin + resin_added) > 160:
                max_resin_time = self.get_max_resin_time(time, set_resin)
                await ctx.send(f"{member_name}'s' resin filled up to full at " + max_resin_time.strftime("%d %b %Y, %H:%M"))
            else:
                current_resin = int(round(self.get_current_resin(time, set_resin)))
                await ctx.send(f'{member_name} currently has {current_resin} resin')
        else:
            await ctx.send(f" I do not have record of {member_name}'s resin")

    @commands.command()
    async def setresin(self, ctx, resin: int):
        """Sets current resin value"""
        error = self.verify_resin(resin)
        if error is not None:
            await ctx.send(f'{error}')
            return
        self.set_current_resin(ctx.author.id, resin)
        additional_msg = ''
        reminders = self.bot.get_cog('Reminders')
        resin_reminder = [r for r in reminders.get_all_reminders(ctx.author) if r.r_type == 'Resin']
        if resin_reminder:
            new_max_time = self.get_max_resin_time(datetime.now(), resin)
            resin_reminder[0].update_time(new_max_time)
            reminders.sort_reminders()
            additional_msg = ' Resin reminder found, readjusted to '+ new_max_time.strftime("%d %b %Y, %H:%M")
        await ctx.send(f'Resin value set to {resin}.{additional_msg}')


    def set_current_resin(self, member_id, current_resin: int):
        self._resin_list[member_id] = {
            'resin': current_resin,
            'time': datetime.now()
            }

    def get_current_resin(self, time, resin: int):
        resin_since = (datetime.now() - time).seconds/(self.resin_rate*60)
        return resin+resin_since

    def clear_resin(self, member_id):
        del self._resin_list[member_id]

    def get_max_resin_time(self, current_time, current_resin: int):
        seconds_to_max = self.get_seconds_to_max(current_resin)
        return current_time + timedelta(seconds=seconds_to_max)

    def get_seconds_to_max(self, resin):
        return (self.max_resin-resin)*self.resin_rate*60

    def verify_resin(self, resin):
        try:
            resin_value = int(resin)
            if resin_value >= 160:
                return 'Max resin value is 160'
        except:
            return f'"{resin}" is not a valid resin value'