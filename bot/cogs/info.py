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
            await ctx.send(f'"{name}" does not seem to be a known character in Tevyat')
            return

        if option.lower() == 'profile':
            image = f'assets/genshin/generated/basic_info_{character.name}.png'
            if os.path.isfile(image):
                await ctx.send(file=discord.File(image))
            else:
                await ctx.send(f'Hold on. Collecting research on {character.name}...')
                await self.generate_basic_info(character)
                await ctx.send(file=discord.File(image))

    async def generate_basic_info(self, ch):
        self.im_p.generate_character_info(ch)