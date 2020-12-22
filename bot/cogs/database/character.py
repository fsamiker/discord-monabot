from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Character, CharacterLevel, CharacterMaterial
from discord.ext import commands
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
import discord
from sqlalchemy.ext.asyncio import AsyncSession

def query_character(session, name):
    stmt = select(Character).\
        options(
            selectinload(Character.special_dish),
            selectinload(Character.talents),
             selectinload(Character.levels),
              selectinload(Character.constellations)).\
                  filter_by(name=name)
    char = session.execute(stmt).scalars().first()
    return char

def query_ascension(session, char_id, starting_lvl, target_lvl):
    stmt = select(CharacterLevel).\
        options(selectinload(CharacterLevel.materials).selectinload(CharacterMaterial.material)).\
            filter(CharacterLevel.character_id==char_id, CharacterLevel.level>=starting_lvl, CharacterLevel.level <=target_lvl).\
            order_by(CharacterLevel.level.asc())
    ascension_list = session.execute(stmt).scalars().all()
    return ascension_list

class Characters(commands.Cog):

    MAX_CHAR_LVL=90
    MIN_CHAR_LVL=1

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def character(self, ctx, name: str, option: str='default'):
        """Get Character Details"""

        option = option.lower()
        name = name.capitalize()

        if option not in ['default', 'talents', 'constellations']:
            raise commands.BadArgument

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            char = await s.run_sync(query_character, name=name)
            if char is None:
                raise NoResultError
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
        if target_lvl > self.MAX_CHAR_LVL:
            await self.send_invalid_input(ctx, f'Character max level is `{self.MAX_CHAR_LVL}`')
            return
        if starting_lvl < self.MIN_CHAR_LVL:
            await self.send_invalid_input(ctx, f'Character levels start at `{self.MIN_CHAR_LVL}`')
            return

        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            char = await s.run_sync(query_character, name=name)
            if char is None:
                raise NoResultError
            asc_list = await s.run_sync(query_ascension, char_id=char.id, starting_lvl=starting_lvl, target_lvl=target_lvl)
            if not asc_list:
                raise NoResultError

            if len(asc_list) == 1:
                footer = f'\nLevel: {asc_list[0].level}'
            else:
                footer = f'\nLevel: {asc_list[0].level} to {asc_list[-1].level}'

            embed = self.get_material_embed(f'{char.name} - Ascension Materials', asc_list, footer, self.bot.get_cog("Flair").get_element_color(char.element))
            file = discord.File(char.icon_url, filename='image.png')
            await ctx.send(file=file, embed=embed)
            return

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
        if character.special_dish:
            dish = character.special_dish.name
        else:
            dish = 'Unknown'
        embed.add_field(name='Special Dish', value=dish)
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

    async def send_invalid_input(self, ctx, reason):
        desc = f'Invalid user input.\n{reason}\nPlease use `{self.bot.command_prefix}help {ctx.command}` for command details'
        await self.bot.get_cog('ErrorHandler').send_error_embed(ctx, 'Command Error', desc)
