from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Character, Talent, TalentLevel
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
    @commands.max_concurrency(5, BucketType.guild, wait=True)
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
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def talentmaterial(self, ctx, name:str, starting_lvl=1, target_lvl=10):
        """Get Talent materials required"""

        async def usage(message):
            examples = '''```Command: talentmaterial <character name> optional:<starting lvl> <target lvl>
Starting Level: Start material count from not including current level (Default: 2)
Starting Level: End material count to level (Default: 10)
Note: 
\u2022 Levels do not include constellation bonuses

Example Usage:
\u2022 m!talent keqing
\u2022 m!talent bennett 8 10```'''

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
            char = s.query(Character).filter_by(name=name).first()
            if not char or not char.talents:
                await ctx.send(f'Could not find details on anyone named "{name}" in my grimoire')
                return
            tal = char.talents[0]
            char_emoji = self.bot.get_cog("Flair").get_emoji(tal.character.name)
            lvl_list = s.query(TalentLevel).\
                filter(TalentLevel.talent_id==tal.id, TalentLevel.level>=starting_lvl, TalentLevel.level <=target_lvl).\
                    order_by(TalentLevel.level.asc()).all()

            if not lvl_list:
                await ctx.send(f'There is no level up available for {char_emoji} {name} in range specified')
                return

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
