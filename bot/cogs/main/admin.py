from discord.ext import commands
import os
import discord

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def server_count_gbg(self, ctx):
        count = len(self.bot.guilds)
        await ctx.send(f'Number of servers in: {count}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def user_count_gbg(self, ctx):
        count = sum([g.member_count for g in self.bot.guilds])
        await ctx.send(f'Number of users in: {count}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def all_stats_gbg(self, ctx):
        g_count = len(self.bot.guilds)
        u_count = sum([g.member_count for g in self.bot.guilds])
        await ctx.send(f'Number of servers in: {g_count}\nNumber of users in: {u_count}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update_status_gbg(self, ctx, option:str='playing', *arg):
        msg = ' '.join(arg)
        if option.lower() == 'playing':
            await self.bot.change_presence(activity=discord.Game(name=msg))
        else:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=msg))

    