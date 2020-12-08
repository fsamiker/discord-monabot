from data.genshin.material import Material
from data.genshin.skill import Skill
from data.genshin.character import Character
from discord.ext import commands
import discord
import json
import os

class Info(commands.Cog):

    def __init__(self, bot, image_processor):
        self.bot = bot
        self.im_p = image_processor

        self.characters = {}
        with open('data/genshin/characters.json', 'r') as f:
            _c = json.load(f)
        for _ in _c:
            c = Character(_)
            self.characters[c.name] = c

        self.skills = {}
        with open('data/genshin/skills.json', 'r') as f:
            _s = json.load(f)
        for _, sk in _s.items():
            s = Skill(sk)
            self.skills[s.name] = s

        self.materials = {}
        with open('data/genshin/materials.json', 'r') as f:
            _m = json.load(f)
        for _, mat in _m.items():
            m = Material(mat)
            self.materials[m.name] = m

    @commands.command()
    async def character(self, ctx, name: str, option: str='Profile'):
        """Get Character Details"""

        character = self.characters.get(name.capitalize())
        if character is None:
            await self.unknown_character(character.name)
            return

        if option.lower() == 'profile':
            image = f'assets/genshin/generated/basic_info_{character.name}.png'
            if os.path.isfile(image):
                await ctx.send(file=discord.File(image))
            else:
                await ctx.send(f'Hold on. Collecting research on {character.name}...')
                await self.generate_basic_info(character)
                await ctx.send(file=discord.File(image))

    @commands.command()
    async def ascensionmaterial(self, ctx, name: str, starting_lvl:int=1, target_lvl:int=90):
        """Get Ascension Materials needed. Command: ascensionmaterial <character name> <start lvl> <end lvl>"""
        character = self.characters.get(name.capitalize())
        if character is None:
            await self.unknown_character(character.name)
            return

        resources = character.get_ascension_resource(starting_lvl, target_lvl)
        lvl_range =resources['Range']
        if not lvl_range:
            await ctx.send(f'There is no ascension available in the select lvl range {starting_lvl} to {target_lvl}')
            return

        if len(lvl_range) == 1:
            output_file = f'assets/genshin/generated/CA_{lvl_range[0]}_{character.name}.png'
            title = f'{character.name} - Ascension Materials Lvl {lvl_range[0]}'
        else:
            output_file = f'assets/genshin/generated/CA_{lvl_range[0]}_{lvl_range[1]}_{character.name}.png'
            title = f'{character.name} - Ascension Materials Lvl {lvl_range[0]} to {lvl_range[1]}'

        icon = character.get_icon()

        if os.path.isfile(output_file):
            await ctx.send(file=discord.File(output_file))
        else:
            await ctx.send(f'Hold on. Collecting research on {character.name}...')
            await self.generate_material_info(icon, title, resources, output_file)
            await ctx.send(file=discord.File(output_file))

    @commands.command()
    async def talentmaterial(self, ctx, name: str, starting_lvl:int=1, target_lvl:int=15):
        """Get Talent Materials needed. Command: talentmaterial <character name> <start lvl> <end lvl>"""
        character = self.characters.get(name.capitalize())
        if character is None:
            await self.unknown_character(character.name)
            return

        resources = character.get_talent_resource(self.skills, starting_lvl, target_lvl)
        lvl_range =resources['Range']
        if not lvl_range:
            await ctx.send(f'Talent lvls only go up to 10. (15 including some constellations)')
            return

        if len(lvl_range) == 1:
            output_file = f'assets/genshin/generated/CTM_{lvl_range[0]}_{character.name}.png'
            title = f'{character.name} - Talent Materials Lvl {lvl_range[0]}'
        else:
            output_file = f'assets/genshin/generated/CTM_{lvl_range[0]}_{lvl_range[1]}_{character.name}.png'
            title = f'{character.name} - Talent Materials Lvl {lvl_range[0]} to {lvl_range[1]}'

        icon = character.get_icon()

        if os.path.isfile(output_file):
            await ctx.send(file=discord.File(output_file))
        else:
            await ctx.send(f'Hold on. Collecting research on {character.name}...')
            await self.generate_material_info(icon, title, resources, output_file)
            await ctx.send(file=discord.File(output_file))
        
    async def generate_basic_info(self, ch):
        self.im_p.generate_character_info(ch)

    async def generate_material_info(self, icon, title, resource, tag):
        self.im_p.generate_materials_needed(icon, title, resource, tag)

    async def unknown_character(self, ctx, name):
        await ctx.send(f'"{name}" does not seem to be a known character in Tevyat')

    def get_all_character_names(self):
        output = [k for k in self.characters.keys()]
        return output