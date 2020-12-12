from data.genshin.models import Talent
from data.db import session_scope
from bot.utils.text import get_texttable
from discord.ext import commands
import discord

class Talents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def talent(self, ctx, *args):
        """Get Talent Details"""

        async def usage(message):
            examples = '''```Command: talent <talent name>

Example Usage:
\u2022 m!talent sharpshooter
\u2022 m!talent Kaboom!```'''
            await ctx.send(f'{message}\n{examples}')

        talent_name = ' '.join([w.capitalize() for w in args])
        with session_scope() as s:
            t = s.query(Talent).filter_by(name=talent_name).first()
            if t:
                file = discord.File(t.icon_url, filename='image.png')
                embed = self.get_talent_basic_info_embed(t)
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find talent "{talent_name}"')

    def get_talent_basic_info_embed(self, talent):
        owner_name = talent.character.name
        color = self.bot.get_cog("Flair").get_element_color(talent.character.element)
        embed = discord.Embed(title=f'{talent.name}', description=f'{talent.description}', color=color)
        embed.add_field(name='Character', value=f'{self.bot.get_cog("Flair").get_emoji(owner_name)} {owner_name}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=f'{talent.typing}')
        return embed
