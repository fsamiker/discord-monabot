import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.cogs.errors import ErrorHandler
from bot.cogs.resin import Resin
from bot.cogs.reminders import Reminders
from bot.cogs.greetings import Greetings
from bot.cogs.admin import Admin
import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Initiate bot
bot = commands.Bot(command_prefix='!f ')

# Add cog modules
bot.add_cog(Greetings(bot))
bot.add_cog(Reminders(bot))
bot.add_cog(Resin(bot))
bot.add_cog(ErrorHandler(bot))
bot.add_cog(Admin(bot, ADMIN_ID))

# Run Bot
bot.run(TOKEN)