from data.genshin.models import Material
from data.db import session_scope
from discord.ext import commands
import discord

class Materials(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def material(self, ctx, *args):
        """Get Material Details"""

        async def usage(message):
            examples = '''```Command: material <material name>

Example Usage:
\u2022 m!material dandelion seed
\u2022 m!material sharp arrowhead```'''
            await ctx.send(f'{message}\n{examples}')


        material_name = ' '.join([w.capitalize() for w in args])
        with session_scope() as s:
            m = s.query(Material).filter_by(name=material_name).first()
            if m:
                file = discord.File(m.icon_url, filename='image.png')
                embed = self.get_material_basic_info_embed(m)
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find material "{material_name}"')

    def get_material_basic_info_embed(self, material):
        desc = ''
        if material.rarity:
            for _ in range(material.rarity):
                desc += f'{self.bot.get_cog("Flair").get_emoji("Star")}'
        desc += f'\n\n{material.description}'

        obtain = ''
        i = 1
        for h in material.how_to_obtain:
            if i != 1:
                obtain += '\n'
            obtain += f'\u2022 {h}'
            i += 1

        embed = discord.Embed(title=f'{material.name}', description=f'{desc}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(name='How to Obtain', value=obtain, inline=False)
        embed.set_footer(text=f'{material.typing}')
        return embed