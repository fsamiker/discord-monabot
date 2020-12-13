from data.genshin.models import Talent, TalentLevel
from data.db import session_scope
from bot.utils.text import get_texttable
from discord.ext import commands
import discord

class Talents(commands.Cog):

    MAX_TAL_LVL=10
    MIN_TAL_LVL=1

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

    @commands.command()
    async def talentmaterial(self, ctx, name:str, starting_lvl=1, target_lvl=10):
        """Get Talent materials required"""

        async def usage(message):
            examples = '''```Command: talent <talent name> optional:<starting lvl> <target lvl>
Note: 
\u2022 Name of talents need to be encapsulated with "<name>" if they are more than one word long
\u2022 Levels do not include constellation bonuses

Example Usage:
\u2022 m!talent sharpshooter
\u2022 m!talent "Kaboom!" 4 10
\u2022 m!talent "passion overload" 8 10```'''

        name = name.title()
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
        if target_lvl > self.MAX_TAL_LVL:
            await usage(f'Current talent max level is {self.MAX_TAL_LVL} (Not including constellations')
            return
        if starting_lvl < self.MIN_TAL_LVL:
            await usage(f'Hey! Are you awake? Talent levels start at {self.MIN_TAL_LVL}')
            return

        with session_scope() as s:
            tal = s.query(Talent).filter_by(name=name).first()
            if tal is None:
                await ctx.send(f'Could not find talent by the name of "{name}" in my grimoire')
                return
            char_emoji = self.bot.get_cog("Flair").get_emoji(tal.character.name)
            lvl_list = s.query(TalentLevel).\
                filter(TalentLevel.talent_id==tal.id, TalentLevel.level>=starting_lvl, TalentLevel.level <=target_lvl).\
                    order_by(TalentLevel.level.asc()).all()

            if not lvl_list:
                await ctx.send(f'There is no level up available for {char_emoji} {name}')
                return

            if len(lvl_list) == 1:
                footer = f'\nLevel: {lvl_list[0].level}'
            else:
                footer = f'\nLevel: {lvl_list[0].level} to {lvl_list[-1].level}'

            embed = self.get_material_embed(f'{char_emoji} {tal.name} - Level Materials',
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
