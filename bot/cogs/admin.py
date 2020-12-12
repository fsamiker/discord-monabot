from discord.ext import commands
import os
import discord

class Admin(commands.Cog):

    def __init__(self, bot, admin_id):
        self.bot = bot
        self.admin_id = int(admin_id)

    def _allowed(self, member):
        return bool(member.id is not None and int(member.id) == self.admin_id)
    