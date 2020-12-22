from bot.utils.error import NoResultError
from sqlalchemy.exc import SQLAlchemyError
from bot.cogs.database.character import query_character
from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Talent, TalentLevel, TalentMaterial
from discord.ext import commands
import discord
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


def query_talent(session, name):
    stmt = select(Talent).options(selectinload(Talent.levels), selectinload(Talent.character)).filter(Talent.name.ilike(f'%{name}%'))
    tal = session.execute(stmt).scalars().first()
    return tal

def query_talentmaterial(session, tal_id, starting_lvl, target_lvl):
    stmt = select(TalentLevel).\
        options(selectinload(TalentLevel.materials).selectinload(TalentMaterial.material)).\
            filter(TalentLevel.talent_id==tal_id, TalentLevel.level>=starting_lvl, TalentLevel.level <=target_lvl).\
            order_by(TalentLevel.level.asc())
    lvl_list = session.execute(stmt).scalars().all()
    return lvl_list

class Talents(commands.Cog):

    MAX_TAL_LVL=10
    MIN_TAL_LVL=1

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def talent(self, ctx, *args):
        """Get Talent Details"""

        if not args:
            raise commands.UserInputError

        talent_name = ' '.join([w.capitalize() for w in args])
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            t = await s.run_sync(query_talent, name=talent_name)
            if t:
                file = discord.File(t.icon_url, filename='image.png')
                embed = self.get_talent_basic_info_embed(t)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def talentmaterial(self, ctx, name:str, starting_lvl=1, target_lvl=10):
        """Get Talent materials required"""

        name = name.title()
        # Check inputs
        try:
            starting_lvl = int(starting_lvl)
            target_lvl = int(target_lvl)
        except:
            raise commands.BadArgument

        if starting_lvl > target_lvl or starting_lvl == target_lvl:
            await self.send_invalid_input(ctx, '`target lvl` should be higher than `starting lvl`')
            return
        if target_lvl > self.MAX_TAL_LVL:
            await self.send_invalid_input(ctx, f'Talent max level is `{self.MAX_TAL_LVL}` (Not including constellations')
            return
        if starting_lvl < self.MIN_TAL_LVL:
            await self.send_invalid_input(ctx, f'Talent levels start at `{self.MIN_TAL_LVL}`')
            return

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            char = await s.run_sync(query_character, name=name)
            if not char or not char.talents:
                raise NoResultError
            tal = char.talents[0]
            char_emoji = self.bot.get_cog("Flair").get_emoji(tal.character.name)
            lvl_list = await s.run_sync(query_talentmaterial, tal_id = tal.id, starting_lvl=starting_lvl, target_lvl=target_lvl)
            if not lvl_list:
                raise NoResultError

            if len(lvl_list) == 1:
                footer = f'\nLevel: {lvl_list[0].level}'
            else:
                footer = f'\nLevel: {lvl_list[0].level} to {lvl_list[-1].level}'

            embed = self.get_material_embed(f'{char_emoji} {char.name} - Talent Level Materials',
             lvl_list,
             footer,
             self.bot.get_cog("Flair").get_element_color(tal.character.element))
            file = discord.File(tal.icon_url, filename='image.png')
            await ctx.send(file=file, embed=embed)
            return

    def get_material_embed(self, title, lvl_list, footer, color):
        mora = sum([l.cost for l in lvl_list])
        embed = discord.Embed(title=f'{title}',
         description=f'\n{self.bot.get_cog("Flair").get_emoji("Mora")} {mora}',
         color=color)
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=footer)
        i = 0
        materials = {}
        for l in lvl_list:
            for m in l.materials:
                if m.material.name in materials.keys():
                    materials[m.material.name] += m.count
                else:
                    materials[m.material.name] = m.count

        for mat, count in materials.items():
            embed.add_field(name=mat, value=f'x{count}', inline=True)
            i += 1

        while (i%3 != 0):
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            i += 1
        
        return embed

    def get_talent_basic_info_embed(self, talent):
        owner_name = talent.character.name
        color = self.bot.get_cog("Flair").get_element_color(talent.character.element)
        embed = discord.Embed(title=f'{talent.name}', description=f'{talent.description}', color=color)
        embed.add_field(name='Character', value=f'{self.bot.get_cog("Flair").get_emoji(owner_name)} {owner_name}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=f'{talent.typing}')
        return embed

    async def send_invalid_input(self, ctx, reason):
        desc = f'Invalid user input.\n{reason}\nPlease use `{self.bot.command_prefix}help {ctx.command}` for command details'
        await self.bot.get_cog('ErrorHandler').send_error_embed(ctx, 'Command Error', desc)
