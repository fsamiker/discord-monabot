import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.cogs.main.errors import ErrorHandler
from bot.cogs.resin import Resin as ResinCog
from bot.cogs.reminders import Reminders as RemindersCog
from bot.cogs.main.greetings import Greetings as GreetingsCog
from bot.cogs.database.talent import Talents as TalentCog
from bot.cogs.database.material import Materials as MaterialCog
from bot.cogs.main.flair import Flair as FlairCog
from bot.cogs.minigame.game import Game as GameCog
from bot.cogs.main.core import Core as CoreCog
from bot.cogs.main.admin import Admin as AdminCog
from bot.cogs.database.character import Characters as CharacterCog
from bot.cogs.database.enemy import Enemies as EnemyCog
from bot.cogs.database.weapon import Weapons as WeaponCog
from bot.cogs.database.artifact import Artifacts as ArtifactCog
from bot.cogs.database.domain import Domains as DomainCog
from bot.cogs.database.core_db import Query as QueryCog
from bot.cogs.minigame.abyss import Abyss as AbyssCog
from bot.cogs.minigame.leaderboards import Leaderboards as LeaderCog
from bot.cogs.main.topgg import Topgg

import os

from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_URI = os.getenv('ASYNC_DB_URI')
TOPGG_TOKEN = os.getenv('TOPGG_TOKEN')

# Set Logging
import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format('logs', 'monabot'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# Initiate bot
bot = commands.Bot(command_prefix='m!', help_command=None)

# Add cog modules
bot.add_cog(CoreCog(bot))
bot.add_cog(GreetingsCog(bot))
bot.add_cog(QueryCog(bot, DB_URI))
bot.add_cog(RemindersCog(bot))
bot.add_cog(ResinCog(bot))
bot.add_cog(AdminCog(bot))
bot.add_cog(CharacterCog(bot))
bot.add_cog(GameCog(bot))
bot.add_cog(AbyssCog(bot))
bot.add_cog(LeaderCog(bot))
bot.add_cog(FlairCog(bot))
bot.add_cog(MaterialCog(bot))
bot.add_cog(TalentCog(bot))
bot.add_cog(EnemyCog(bot))
bot.add_cog(WeaponCog(bot))
bot.add_cog(ArtifactCog(bot))
bot.add_cog(DomainCog(bot))
bot.add_cog(Topgg(bot, TOPGG_TOKEN))
bot.add_cog(ErrorHandler(bot))

# Run Bot
bot.run(TOKEN)