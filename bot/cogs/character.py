from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Character, CharacterLevel
from data.db import session_scope
from discord.ext import commands
import discord
import os

class Characters(commands.Cog):

    MAX_CHAR_LVL=90
    MIN_CHAR_LVL=1

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def character(self, ctx, name: str, option: str='default'):
        """Get Character Details"""

        async def usage(message):
            examples = '''```Command: character <character name> optional: <option>          
Options: \u2022 default - Character basic information
         \u2022 talents - Character talent list
         \u2022 constellations - Character constellations list

Example Usage:
\u2022 m!character amber
\u2022 m!character bennett talents
\u2022 m!character keqing constellations```'''
            await ctx.send(f'{message}\n{examples}')

        option = option.lower()
        name = name.capitalize()

        if option not in ['default', 'talents', 'constellations']:
            await usage('Invalid command')

        with session_scope() as s:
            char = s.query(Character).filter_by(name=name).first()
            if char is None:
                await self.unknown_character(ctx, name)
                return
            icon_file = discord.File(char.icon_url, filename='image.png')
            if option == 'default':
                embed = self.get_character_basic_embed(char)
                await ctx.send(file=icon_file, embed=embed)
            elif option == 'talents':
                talents = char.talents
                embed = self.get_talents_embed(talents, char)
                await ctx.send(file=icon_file, embed=embed)
            elif option == 'constellations':
                embed = self.get_constellations_embed(char.constellations, char)
                await ctx.send(file=icon_file, embed=embed)

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def ascensionmaterial(self, ctx, name: str, starting_lvl=1, target_lvl=90):
        """Get Ascension Materials needed"""

        async def usage(message):
            examples = '''```Command: ascensionmaterial <character name> optional:<start lvl> <end lvl>          
Start Lvl: Start counting from character level (Default:1)
End Lvl: Stop counting at character level (Default:90)

Example Usage:
\u2022 m!ascensionmaterial amber
\u2022 m!ascensionmaterial amber 1 90
\u2022 m!ascensionmaterial amber 45 87```'''
            await ctx.send(f'{message}\n{examples}')

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
        if target_lvl > self.MAX_CHAR_LVL:
            await usage(f'Current character max level is {self.MAX_CHAR_LVL}')
            return
        if starting_lvl < self.MIN_CHAR_LVL:
            await usage(f'Hey! Are you awake? Character levels start at {self.MIN_CHAR_LVL}')
            return

        with session_scope() as s:
            char = s.query(Character).filter_by(name=name).first()
            if char is None:
                await self.unknown_character(ctx, name)
                return
            asc_list = s.query(CharacterLevel).\
                filter(CharacterLevel.character_id==char.id, CharacterLevel.level>=starting_lvl, CharacterLevel.level <=target_lvl).\
                    order_by(CharacterLevel.level.asc()).all()

            if not asc_list:
                await ctx.send(f'There is no ascension available in the lvl range {starting_lvl} to {target_lvl}')
                return

            if len(asc_list) == 1:
                footer = f'\nLevel: {asc_list[0].level}'
            else:
                footer = f'\nLevel: {asc_list[0].level} to {asc_list[-1].level}'

            embed = self.get_material_embed(f'{char.name} - Ascension Materials', asc_list, footer, self.bot.get_cog("Flair").get_element_color(char.element))
            file = discord.File(char.icon_url, filename='image.png')
            await ctx.send(file=file, embed=embed)
            return

    async def unknown_character(self, ctx, name):
        await ctx.send(f'"{name}" does not seem to be a known character in Tevyat')

    def get_material_embed(self, title, ascension_list, footer, color):
        mora = sum([a.cost for a in ascension_list])
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

    def get_character_basic_embed(self, character):
        rarity = ''
        if character.rarity:
            for _ in range(character.rarity):
                rarity += f'{self.bot.get_cog("Flair").get_emoji("Star")}'
        embed = discord.Embed(title=f'{self.bot.get_cog("Flair").get_emoji(character.element)} {character.name}',
         description=f'{rarity}',
         color=self.bot.get_cog("Flair").get_element_color(character.element))
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(name='Weapon', value=character.weapon_type)
        embed.add_field(name='Region', value=character.region)
        embed.add_field(name='Birthday', value=character.birthday)
        embed.add_field(name='Affiliation', value=character.affiliation)
        embed.add_field(name='Special Dish', value=character.special_dish.name)
        embed.add_field(name='\u200b', value='\u200b')
        return embed

    def get_talents_embed(self, talents, character):
        embed = discord.Embed(title=f'{self.bot.get_cog("Flair").get_emoji(character.element)} {character.name} - Talent List',
        color=self.bot.get_cog("Flair").get_element_color(character.element),
        description=f"These are {character.name}'s talents\nFor further information run m!talent <talent name>")
        embed.add_field(name='Name', value=f'{talents[0].name}', inline=True)
        embed.add_field(name='Type', value=f'{talents[0].typing.replace("Talent", "")}', inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        for t in talents[1:]:
            embed.add_field(name='\u200b', value=f'{t.name}', inline=True)
            embed.add_field(name='\u200b', value=f'{t.typing.replace("Talent", "")}', inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)

        embed.set_thumbnail(url='attachment://image.png')
        return embed

    def get_constellations_embed(self, constellations, character):
        embed = discord.Embed(title=f'{self.bot.get_cog("Flair").get_emoji(character.element)} {character.name} - Constellation List',
        color=self.bot.get_cog("Flair").get_element_color(character.element))
        embed.add_field(name='Constellation', value=f'C{constellations[0].level}', inline=True)
        embed.add_field(name='Name', value=f'{constellations[0].name}', inline=True)
        embed.add_field(name='Effect', value=f'{constellations[0].effect}', inline=True)

        for c in constellations[1:]:
            embed.add_field(name='\u200b', value=f'C{c.level}', inline=True)
            embed.add_field(name='\u200b', value=f'{c.name}', inline=True)
            embed.add_field(name='\u200b', value=f'{c.effect}', inline=True)

        embed.set_thumbnail(url='attachment://image.png')
        return embed
