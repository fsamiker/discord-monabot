from data.db import session_scope
import discord
from datetime import datetime, timedelta
from discord.ext import commands
from data.monabot.models import Reminder, Resin as resinmodel
import math

class Resin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.max_resin = 160
        self.resin_rate = 8  #minutes

    @commands.command()
    async def checkresin(self, ctx, member: discord.Member=None):
        """Shows current resin value. Blank for self or Tag a user"""

        # Resin Target User
        if member is None:
            member = ctx.message.author
        member_id = member.id
        member_name = member.display_name
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        # Prepare embded
        embed = discord.Embed(title=f"{member_name.capitalize()}'s Resin",
        color=discord.Colour.dark_blue())

        # Get User Resin
        with session_scope() as s:
            resin = s.query(resinmodel).filter_by(discord_id=member_id).first()
            if not resin:
                embed.description = 'No Record'
                embed.set_footer(text='Run m!setresin to record resin')
            else:
                max_resin_time = self.get_max_resin_time(resin.timestamp, resin.resin)
                display_time = self.convert_from_utc(max_resin_time, server_region).strftime("%I:%M %p, %d %b %Y")
                now = datetime.utcnow()
                if max_resin_time < now:
                    embed.add_field(name= f'{self.bot.get_cog("Flair").get_emoji("Resin")} 160', value='\u200b')
                else:
                    current_resin = self.get_current_resin(resin.timestamp, resin.resin)
                    embed.add_field(name= f'{self.bot.get_cog("Flair").get_emoji("Resin")} {current_resin}', value='\u200b')
                embed.set_footer(text=f'Max Resin At: {display_time}')
        
        await ctx.send(embed=embed)

    @commands.command()
    async def setresin(self, ctx, resin):
        """Sets current resin value"""

        # Verify resin value
        error = self.verify_resin(resin)
        if error is not None:
            await ctx.send(f'{error}')
            return

        message = ''
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'
        resin = int(resin)

        # Prepare embded
        flair = self.bot.get_cog("Flair")
        embed = discord.Embed(title=f"{ctx.author.display_name.capitalize()}'s Resin",
        color=discord.Colour.dark_blue())
        desc = ''

        with session_scope() as s:
            # check for existing resin
            r = s.query(resinmodel).filter_by(discord_id=ctx.author.id).first()
            now = datetime.utcnow()
            max_resin_time = self.get_max_resin_time(now, resin)
            display_time = self.convert_from_utc(max_resin_time, server_region).strftime("%I:%M %p, %d %b %Y")
            embed.set_footer(text=f'Max Resin At: {display_time}')
            if r:
                embed.add_field(name= f'{flair.get_emoji("Resin")} {r.resin} -> {resin}', value='\u200b')
                r.resin = resin
                r.timestamp = now
                # check for existing reminder
                reminder = s.query(Reminder).filter_by(discord_id=ctx.author.id, typing='Max Resin').first()
                if reminder:
                    reminder.when=max_resin_time
                    reminder.timezone=server_region
                    reminder.channel=ctx.channel.id
                    desc += f"\n{flair.get_emoji('Reminder')} 'Max Resin' reminder adjusted to {display_time}"
            else:
                # set new entry
                r = resinmodel(
                    discord_id=ctx.author.id,
                    resin=resin,
                    timestamp=datetime.utcnow()
                )
                s.add(r)
                desc += f'Set current resin value'
                embed.add_field(name= f'{flair.get_emoji("Resin")} {resin}', value='\u200b')
            
        embed.description = desc.strip()

        self.bot.get_cog('Reminders')._get_next_reminder()
        
        await ctx.send(embed=embed)

    @commands.command()
    async def timetoresin(self, ctx, resin_value, member:discord.Member=None):
        """Get time of particular resin value"""

        # Verify resin value
        error = self.verify_resin(resin_value)
        if error is not None:
            await ctx.send(f'{error}')
            return
        resin_value = int(resin_value)

        # Resin Target User
        if member is None:
            member = ctx.message.author
        member_id = member.id
        member_name = member.display_name
        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

        # Prepare embded
        embed = discord.Embed(title=f"{member_name.capitalize()}'s Resin",
        color=discord.Colour.dark_blue())

        # Get User Resin
        with session_scope() as s:
            resin = s.query(resinmodel).filter_by(discord_id=member_id).first()
            if not resin:
                embed.description = 'No Record'
                embed.set_footer(text='Run m!setresin to record resin')
            else:
                resin_time = self.get_resin_time(resin.timestamp, resin.resin, resin_value)
                display_time = self.convert_from_utc(resin_time, server_region).strftime("%I:%M %p, %d %b %Y")
                now = datetime.utcnow()
                if resin_time < now:
                    embed.description = 'You are already at max resin'
                    embed.add_field(name= f'{self.bot.get_cog("Flair").get_emoji("Resin")} 160', value='\u200b')
                else:
                    embed.description = f'You will reach {self.bot.get_cog("Flair").get_emoji("Resin")}{resin_value} at {display_time}'
                    current_resin = self.get_current_resin(resin.timestamp, resin.resin)
                    embed.add_field(name= f'Current {self.bot.get_cog("Flair").get_emoji("Resin")}: {current_resin}', value='\u200b')
                max_resin_time = self.get_max_resin_time(now, resin.resin)
                max_display_time = self.convert_from_utc(max_resin_time, server_region).strftime("%I:%M %p, %d %b %Y")    
                embed.set_footer(text=f'Max Resin At: {max_display_time}')
        
        await ctx.send(embed=embed)

    def get_current_resin(self, time, resin: int):
        resin_since = (datetime.utcnow() - time).seconds/(self.resin_rate*60)
        return math.floor(resin+resin_since)

    def clear_resin(self, member_id):
        del self._resin_list[member_id]

    def get_max_resin_time(self, current_time, current_resin: int):
        seconds_to_max = self.get_seconds_to_resin(current_resin)
        return current_time + timedelta(seconds=seconds_to_max)

    def get_resin_time(self, current_time, current_resin, target_resin):
        seconds_to = self.get_seconds_to_resin(current_resin, target_resin)
        return current_time + timedelta(seconds=seconds_to)

    def get_seconds_to_resin(self, resin, final_resin=160):
        return (final_resin-resin)*self.resin_rate*60

    def verify_resin(self, resin):
        try:
            resin_value = int(resin)
            if resin_value >= 160:
                return 'Max resin value is 160'
        except:
            return f'"{resin}" is not a valid resin value'

    def convert_from_utc(self, time, server_region):
        reminder_cog = self.bot.get_cog('Reminders')
        return reminder_cog.convert_from_utc(time, server_region)
