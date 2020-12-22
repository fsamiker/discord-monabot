from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy.exc import SQLAlchemyError
from data.genshin.models import Weapon, WeaponLevel, WeaponMaterial
from discord.ext import commands
import discord
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

def query_weapon(session, name):
    stmt = select(Weapon).options(selectinload(Weapon.levels)).filter(Weapon.name.like(f'%{name}%'))
    wp = session.execute(stmt).scalars().first()
    return wp

def query_weaponascension(session, weapon_id, starting_lvl, target_lvl):
    stmt = select(WeaponLevel).\
        options(selectinload(WeaponLevel.materials).selectinload(WeaponMaterial.material)).\
            filter(WeaponLevel.weapon_id==weapon_id, WeaponLevel.level>=starting_lvl, WeaponLevel.level <=target_lvl).\
            order_by(WeaponLevel.level.asc())
    asc_list = session.execute(stmt).scalars().all()
    return asc_list

class Weapons(commands.Cog):

    MAX_WP_LVL=90
    MIN_WP_LVL=1

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def weapon(self, ctx, *args):
        """Get Weapon Details"""

        if not args:
            raise commands.UserInputError

        name = ' '.join([w.capitalize() for w in args])

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            wp = await s.run_sync(query_weapon, name=name)
            if wp:
                file = discord.File(wp.icon_url, filename='image.png')
                embed = self.get_weapon_info_embed(wp)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def weaponmaterial(self, ctx, *args):
        """Get Weapon Details"""
            
        if not args:
            raise commands.UserInputError

        name = ' '.join([w.capitalize() for w in args])
        starting_lvl = 1
        target_lvl = 90
        try:
            starting_lvl = int(args[-2])
            target_lvl = int(args[-1])
            name = ' '.join([w.capitalize() for w in args[:-2]])
        except:
            pass
        
        # Check inputs
        try:
            starting_lvl = int(starting_lvl)
            target_lvl = int(target_lvl)
        except:
            raise commands.BadArgument

        if starting_lvl > target_lvl or starting_lvl == target_lvl:
            await self.send_invalid_input(ctx, '`target lvl` should be higher than `starting lvl`')
            return
        if target_lvl > self.MAX_WP_LVL:
            await self.send_invalid_input(ctx, f'Weapon max level is `{self.MAX_WP_LVL}`')
            return
        if starting_lvl < self.MIN_WP_LVL:
            await self.send_invalid_input(ctx, f'Weapon levels start at `{self.MIN_WP_LVL}`')
            return

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            wp = await s.run_sync(query_weapon, name=name)
            if wp:
                asc_list = await s.run_sync(query_weaponascension, weapon_id=wp.id, starting_lvl=starting_lvl, target_lvl=target_lvl)
                if not asc_list:
                    raise NoResultError

                if len(asc_list) == 1:
                    footer = f'\nLevel: {asc_list[0].level}'
                else:
                    footer = f'\nLevel: {asc_list[0].level} to {asc_list[-1].level}'

                embed = self.get_material_embed(f'{wp.name} - Ascension Materials', asc_list, footer, discord.Colour.dark_red())
                file = discord.File(wp.icon_url, filename='image.png')
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

    def get_weapon_info_embed(self, weapon):
        flair = self.bot.get_cog("Flair")
        rarity = ''
        if weapon.rarity:
            for _ in range(weapon.rarity):
                rarity += f'{flair.get_emoji("Star")}'
        desc = f'{rarity}\n\n{weapon.description}'
        embed = discord.Embed(title=f'{weapon.name}', description=desc, color=discord.Colour.dark_red())
        embed.add_field(name='Type', value=weapon.typing)
        embed.add_field(name='Series', value=weapon.series)
        embed.add_field(name='Secondary Stat', value=weapon.secondary_stat)
        embed.add_field(name='Effect', value=weapon.effect)
        embed.set_thumbnail(url='attachment://image.png')
        return embed


    def get_material_embed(self, title, ascension_list, footer, color):
        mora = sum([a.cost for a in ascension_list if a.cost])
        embed = discord.Embed(title=f'{title}',
         description=f'\n{self.bot.get_cog("Flair").get_emoji("Mora")} {mora}',
         color=color)
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=footer)
        i = 0
        materials = {}
        for a in ascension_list:
            for m in a.materials:
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

    async def send_invalid_input(self, ctx, reason):
        desc = f'Invalid user input.\n{reason}\nPlease use `{self.bot.command_prefix}help {ctx.command}` for command details'
        await self.bot.get_cog('ErrorHandler').send_error_embed(ctx, 'Command Error', desc)