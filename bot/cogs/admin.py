from discord.ext import commands
import os
import discord

class Admin(commands.Cog):

    def __init__(self, bot, admin_id):
        self.bot = bot
        self.admin_id = int(admin_id)

    def _allowed(self, member):
        return bool(member.id is not None and int(member.id) == self.admin_id)

    @commands.command(hidden=True)
    async def monaspeaks(self, ctx, *args):
        member = ctx.author

        if not self._allowed(member):
            return
        await ctx.send(' '.join(args))

    @commands.command(hidden=True)
    async def serverdown(self, ctx):
        member = ctx.author

        if not self._allowed(member):
            return

        await ctx.send('Server going down for awhile!')

    @commands.command(hidden=True)
    async def serverup(self, ctx):
        member = ctx.author

        if not self._allowed(member):
            return

        await ctx.send('Server is back up!')