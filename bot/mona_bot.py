import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.cogs.errors import ErrorHandler
from bot.cogs.resin import Resin as ResinCog
from bot.cogs.reminders import Reminders as RemindersCog
from bot.cogs.greetings import Greetings as GreetingsCog
from bot.cogs.talent import Talents as TalentCog
from bot.cogs.material import Materials as MaterialCog
from bot.cogs.flair import Flair as FlairCog
from bot.cogs.game import Game as GameCog
from bot.cogs.core import Core as CoreCog
from bot.cogs.admin import Admin as AdminCog
from bot.cogs.character import Characters as CharacterCog
from bot.cogs.enemy import Enemies as EnemyCog
from bot.cogs.weapon import Weapons as WeaponCog
from bot.cogs.artifact import Artifacts as ArtifactCog
from bot.cogs.domain import Domains as DomainCog

import os

from dotenv import load_dotenv
from discord.ext import commands
import discord

from data.db import *
from data.genshin.models import *
from data.monabot.models import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initiate bot
intents = discord.Intents.default()
intents.members = True
intents.guilds=True
bot = commands.Bot(command_prefix='m!', intents=intents, help_command=None)

# Add cog modules
bot.add_cog(CoreCog(bot))
bot.add_cog(GreetingsCog(bot))
bot.add_cog(RemindersCog(bot))
bot.add_cog(ResinCog(bot))
bot.add_cog(AdminCog(bot))
bot.add_cog(CharacterCog(bot))
bot.add_cog(GameCog(bot))
bot.add_cog(FlairCog(bot))
bot.add_cog(MaterialCog(bot))
bot.add_cog(TalentCog(bot))
bot.add_cog(EnemyCog(bot))
bot.add_cog(WeaponCog(bot))
bot.add_cog(ArtifactCog(bot))
bot.add_cog(DomainCog(bot))

# Run Bot
bot.run(TOKEN)