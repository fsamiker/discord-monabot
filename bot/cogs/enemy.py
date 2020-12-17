from data.genshin.models import Enemy
from data.db import session_scope
from  sqlalchemy.sql.expression import func
from discord.ext import commands
import discord

class Enemies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enemy(self, ctx, *args):
        """Get Enemy/Boss Details"""

        async def usage(message):
            examples = '''```Command: enemy <enemy name>

Example Usage:
\u2022 m!enemy hilichurls
\u2022 m!enemy dvalin```'''
            await ctx.send(f'{message}\n{examples}')

        enemy_name = ' '.join([w.capitalize() for w in args])
        with session_scope() as s:
            e = s.query(Enemy).filter(Enemy.name.like(f'%{enemy_name}%')).first()
            if e:
                file = discord.File(e.icon_url, filename='image.png')
                embed = self.get_enemy_info_embed(e)
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find details on "{enemy_name}"')

    def get_enemy_info_embed(self, enemy):
        var = ''
        if enemy.variants:
            var += '\u2022 '
            var += '\n\u2022 '.join(enemy.get_variants())

        drops = ''
        i = 1
        for m in enemy.material_drops:
            if i != 1:
                drops += '\n'
            drops += f'\u2022 {m.name}'
            i += 1

        embed = discord.Embed(title=f'{enemy.name}', color=discord.Colour.purple())
        embed.set_thumbnail(url='attachment://image.png')
        if var:
            embed.add_field(name='Variants', value=var, inline=False)
        if drops:
            embed.add_field(name='Possible Material Drops', value=drops, inline=False)
        embed.set_footer(text=f'Type: {enemy.typing}')
        return embed