from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy.exc import SQLAlchemyError
from data.genshin.models import Enemy
from discord.ext import commands
import discord
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

def query_enemy(session, name):
    stmt = select(Enemy).options(selectinload(Enemy.material_drops)).filter(Enemy.name.ilike(f'%{name}%'))
    enem = session.execute(stmt).scalars().first()
    return enem

class Enemies(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def enemy(self, ctx, *args):
        """Get Enemy/Boss Details"""

        if not args:
            raise commands.UserInputError

        enemy_name = ' '.join([w.capitalize() for w in args])
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            e = await s.run_sync(query_enemy, name=enemy_name)
            if e:
                file = discord.File(e.icon_url, filename='image.png')
                embed = self.get_enemy_info_embed(e)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

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