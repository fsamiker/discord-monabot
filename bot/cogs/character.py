from data.genshin.models import Character
from data.db import session_scope
from discord.ext import commands
import discord
import os

class Characters(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def character(self, ctx, name: str, option: str='default'):
        """Get Character Details"""

        async def usage(message):
            examples = '''```Command: character <character name> optional: <option>          
Options: \u2022 default - Character basic information text
         \u2022 image - Character basic information image
         \u2022 talents - Character talent list
         \u2022 constellations - Character constellations list

Example Usage:
\u2022 m!character amber
\u2022 m!character zhongli image
\u2022 m!character bennett talents
\u2022 m!character keqing constellations```'''
            await ctx.send(f'{message}\n{examples}')

        option = option.lower()
        name = name.capitalize()

        if option not in ['default', 'image', 'talents', 'constellations']:
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
            elif option == 'image':
                if char.profile_url:
                    await ctx.send(file=discord.File(char.profile_url))
                else:
                    await ctx.send(f'Could not find profile image for {char.name}')
            elif option == 'talents':
                talents = char.talents
                embed = self.get_talents_embed(talents, char)
                await ctx.send(file=icon_file, embed=embed)
            elif option == 'constellations':
                embed = self.get_constellations_embed(char.constellations, char)
                await ctx.send(file=icon_file, embed=embed)

    @commands.command()
    async def ascensionmaterial(self, ctx, name: str, *args):
        """Get Ascension Materials needed"""

        async def usage(message):
            examples = '''```Command: ascensionmaterial <character name> optional:<start lvl> <end lvl> <option>          
Start Lvl: Start counting from character level (Default:1)
End Lvl: Stop counting at character level (Default:90)
Options: \u2022 default - Text list
         \u2022 image - Image Form

Example Usage:
\u2022 m!ascensionmaterial amber
\u2022 m!ascensionmaterial amber 1 90
\u2022 m!ascensionmaterial amber 45 87```'''
            await ctx.send(f'{message}\n{examples}')

        # Check Inputs
        character = self.characters.get(name.capitalize())
        if character is None:
            await self.unknown_character(name)
            return

        starting_lvl = 1  # Default value
        target_lvl = 90  # Default value
        option = 'default'  # Default value
        if len(args) > 3:
            await usage('Invalid command')
            return
        if len(args) >= 2:
            try:
                starting_lvl = int(args[0])
                target_lvl = int(args[1])
            except:
                await usage('Invalid command')
                return
        if starting_lvl > target_lvl:
            await usage('Starting Level cannot be higher than End Level')
        if len(args) == 3 or len(args) == 1:
            option = args[-1].lower()
            if option not in ['image', 'default']:
                await usage('Invalid options')
                return

        resources = character.get_ascension_resource(starting_lvl, target_lvl)
        lvl_range =resources['Range']
        if not lvl_range:
            await ctx.send(f'There is no ascension available in the lvl range {starting_lvl} to {target_lvl}')
            return

        if len(lvl_range) == 1:
            output_file = f'assets/genshin/generated/CA_{lvl_range[0]}_{character.name}.png'
            title = f'{character.name} - Ascension Materials'
            footer = f'\nLevel: {lvl_range[0]}'
        else:
            output_file = f'assets/genshin/generated/CA_{lvl_range[0]}_{lvl_range[1]}_{character.name}.png'
            title = f'{character.name} - Ascension Materials'
            footer = f'\nLevel: {lvl_range[0]} to {lvl_range[1]}'

        icon = character.get_icon()
        embed = self.get_material_embed(title, resources, footer)
        if option.lower() == 'default':
            file = discord.File(icon, filename='image.png')
            await ctx.send(file=file, embed=embed)
            return

        elif option.lower() == 'image':
            icon = character.get_icon()

            if os.path.isfile(output_file):
                await ctx.send('These are the materials needed...',file=discord.File(output_file))
            else:
                await ctx.send(f'Hold on. Collecting research on {name}...')
                await self.generate_material_info(icon, title, resources, output_file)
                await ctx.send('These are the materials needed...',file=discord.File(output_file))

    @commands.command()
    async def talentmaterial(self, ctx, name: str, *args):
        """Get Talent Materials needed"""

        async def usage(message):
            examples = '''```Command: talentmaterial <character name> optional:<start lvl> <end lvl> <option>          
Start Lvl: Start counting from talent level (Default:1)
End Lvl: Stop counting at talent level (Default:15)
Options: \u2022 default - Text list
         \u2022 image - Image Form

Example Usage:
\u2022 m!talentmaterial amber
\u2022 m!talentmaterial amber 2 15
\u2022 m!talentmaterial amber 1 10```'''
            await ctx.send(f'{message}\n{examples}')

        # Check Inputs
        character = self.characters.get(name.capitalize())
        if character is None:
            await self.unknown_character(name)
            return

        starting_lvl = 1  # Default value
        target_lvl = 15  # Default value
        option = 'default'  # Default value
        if len(args) > 3:
            await usage('Invalid command')
            return
        if len(args) >= 2:
            try:
                starting_lvl = int(args[0])
                target_lvl = int(args[1])
            except:
                await usage('Invalid command')
                return
        if starting_lvl > target_lvl:
            await usage('Starting Level cannot be higher than End Level')
        if len(args) == 3 or len(args) == 1:
            option = args[-1].lower()
            if option not in ['image', 'default']:
                await usage('Invalid command')
                return

        # Collect Data
        resources = character.get_talent_resource(self.skills, starting_lvl, target_lvl)
        lvl_range =resources['Range']
        if not lvl_range:
            await usage(f'Talent lvls only go up to 10. (15 including some constellations)')
            return

        if len(lvl_range) == 1:
            output_file = f'assets/genshin/generated/CTM_{lvl_range[0]}_{character.name}.png'
            title = f'{character.name} - Talent Materials'
            footer = f'\nLevel: {lvl_range[0]}'
        else:
            output_file = f'assets/genshin/generated/CTM_{lvl_range[0]}_{lvl_range[1]}_{character.name}.png'
            title = f'{character.name} - Talent Materials'
            footer = f'\nLevel: {lvl_range[0]} to {lvl_range[1]}'

        icon = character.get_icon()
        embed = self.get_material_embed(title, resources, footer)
        if option.lower() == 'default':
            file = discord.File(icon, filename='image.png')
            await ctx.send(file=file, embed=embed)
            return
        elif option.lower() == 'image':
            if os.path.isfile(output_file):
                await ctx.send('These are the materials needed...',file=discord.File(output_file))
            else:
                await ctx.send(f'Hold on. Collecting research on {character.name}...')
                await self.generate_material_info(icon, title, resources, output_file)
                await ctx.send(f'These are the materials needed...',file=discord.File(output_file))

    async def unknown_character(self, ctx, name):
        await ctx.send(f'"{name}" does not seem to be a known character in Tevyat')

    def get_material_embed(self, title, resources, footer):
        emojis = self.bot.get_cog('Emoji').emojis
        embed = discord.Embed(title=f'{title}', description=f'{emojis.get("Mora")} {resources["Mora"]}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=footer)
        i = 0
        for mat, count in resources["Materials"].items():
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
        embed.add_field(name='Special Dish', value=character.special_dish)
        embed.add_field(name='\u200b', value='\u200b')
        return embed

    def get_talents_embed(self, talents, character):
        embed = discord.Embed(title=f'{self.bot.get_cog("Flair").get_emoji(character.element)} {character.name} - Talent List',
        color=self.bot.get_cog("Flair").get_element_color(character.element))
        embed.add_field(name='Name', value=f'{talents[0].name}', inline=True)
        embed.add_field(name='Type', value=f'{talents[0].typing.replace("Talent", "")}', inline=True)
        embed.add_field(name='Description', value=f'{talents[0].description}', inline=True)

        for t in talents[1:]:
            embed.add_field(name='\u200b', value=f'{t.name}', inline=True)
            embed.add_field(name='\u200b', value=f'{t.typing.replace("Talent", "")}', inline=True)
            embed.add_field(name='\u200b', value=f'{t.description}', inline=True)

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
