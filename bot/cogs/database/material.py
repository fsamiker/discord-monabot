from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy.exc import SQLAlchemyError
from data.genshin.models import Food, Material
from  sqlalchemy.sql.expression import func
from discord.ext import commands
import discord
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

def query_materials(session, name):
    stmt = select(Material).filter(Material.name.ilike(f'%{name}%'))
    mat = session.execute(stmt).scalars().first()
    return mat

def query_foods(session, name):
    stmt = select(Food).options(selectinload(Food.specialty_of)).filter(Food.name.ilike(f'%{name}%'))
    food = session.execute(stmt).scalars().first()
    return food

class Materials(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def material(self, ctx, *args):
        """Get Material Details"""

        if not args:
            raise commands.UserInputError


        material_name = ' '.join([w.capitalize() for w in args])
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            m = await s.run_sync(query_materials, name=material_name)
            if m:
                file = discord.File(m.icon_url, filename='image.png')
                embed = self.get_material_basic_info_embed(m)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def food(self, ctx, *args):
        """Get Food Details"""

        food_name = ' '.join([w.capitalize() for w in args])
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            f = await s.run_sync(query_foods, name=food_name)
            if f:
                file = discord.File(f.icon_url, filename='image.png')
                embed = self.get_food_basic_info_embed(f)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

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

    def get_food_basic_info_embed(self, food):
        desc = ''
        if food.rarity:
            for _ in range(food.rarity):
                desc += f'{self.bot.get_cog("Flair").get_emoji("Star")}'
        desc += f'\n\n{food.description}'

        embed = discord.Embed(title=f'{food.name}', description=f'{desc}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(name='Effect', value=food.effect, inline=False)
        embed.add_field(name='Type', value=f'{food.typing}', inline=True)
        if food.specialty_of:
            embed.add_field(name='Specialty Of', value=f'{food.specialty_of.name}', inline=True)
        return embed