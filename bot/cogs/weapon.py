from data.genshin.models import Weapon, WeaponLevel
from data.db import session_scope
from discord.ext import commands
import discord
import os

class Weapons(commands.Cog):

    MAX_WP_LVL=90
    MIN_WP_LVL=1

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weapon(self, ctx, *args):
        """Get Weapon Details"""

        async def usage(message):
            examples = '''```Command: weapon <weapon name>          

Example Usage:
\u2022 m!weapon Amos' Bow
\u2022 m!weapon prototype rancour```'''
            await ctx.send(f'{message}\n{examples}')

        name = ' '.join([w.capitalize() for w in args])

        with session_scope() as s:
            wp = s.query(Weapon).filter(Weapon.name.like(f'%{name}%')).first()
            if wp:
                file = discord.File(wp.icon_url, filename='image.png')
                embed = self.get_weapon_info_embed(wp)
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find weapon "{name}"')

    @commands.command()
    async def weaponmaterial(self, ctx, *args):
        """Get Weapon Details"""

        async def usage(message):
            examples = '''```Command: weaponmaterial <weapon name> optional:<starting lvl> <target lvl>
Starting Level: Start material count from not including current level (Default: 1)
Starting Level: End material count to level (Default: 90)

Example Usage:
\u2022 m!weaponmaterial solar pearl
\u2022 m!weaponmaterial skyward harp 5 10```'''

            await ctx.send(f'{message}\n{examples}')

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
            await usage('Invalid command')
            return

        if starting_lvl > target_lvl or starting_lvl == target_lvl:
            await usage('Target Level should be higher than Starting Level')
            return
        if target_lvl > self.MAX_WP_LVL:
            await usage(f'Weapon max level is {self.MAX_WP_LVL}')
            return
        if starting_lvl < self.MIN_WP_LVL:
            await usage(f'Hey! Are you awake? Weapon levels start at {self.MIN_WP_LVL}')
            return

        with session_scope() as s:
            wp = s.query(Weapon).filter(Weapon.name.like(f'%{name}%')).first()
            if wp:
                asc_list = s.query(WeaponLevel).\
                    filter(WeaponLevel.weapon_id==wp.id, WeaponLevel.level>=starting_lvl, WeaponLevel.level <=target_lvl).\
                        order_by(WeaponLevel.level.asc()).all()

                if not asc_list:
                    await ctx.send(f'There is no ascension available in the lvl range {starting_lvl} to {target_lvl}')
                    return

                if len(asc_list) == 1:
                    footer = f'\nLevel: {asc_list[0].level}'
                else:
                    footer = f'\nLevel: {asc_list[0].level} to {asc_list[-1].level}'

                embed = self.get_material_embed(f'{wp.name} - Ascension Materials', asc_list, footer, discord.Colour.dark_red())
                file = discord.File(wp.icon_url, filename='image.png')
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find weapon "{name}"')

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