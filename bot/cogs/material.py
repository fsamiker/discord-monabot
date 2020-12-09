from discord.ext import commands
import discord

class Material(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.materials = self.bot.get_cog('Character').materials

    @commands.command()
    async def material(self, ctx, *args):
        """Get Material Details"""

        async def usage(message):
            examples = '''```Command: character <material name>

Example Usage:
\u2022 m! dandelion seed
\u2022 m! sharp arrowhead```'''
            await ctx.send(f'{message}\n{examples}')

        if any([type(w)!=str for w in args]):
            await usage('Invalid command')

        material_name = ' '.join([w.capitalize() for w in args])
        if material_name not in self.materials.keys():
            await ctx.send(f'Could not find material "{material_name}"')

        material = self.materials.get(material_name)

        file = discord.File(material.get_icon(), filename='image.png')
        embed = self.get_material_basic_info_embed(material)
        await ctx.send(file=file, embed=embed)

    def get_material_basic_info_embed(self, material):
        emojis = self.bot.get_cog('Emoji').emojis
        desc = ''
        for _ in range(material.rarity):
            desc += f'{emojis.get("Star")}'
        desc += f'\n\n{material.description}'

        obtain = ''
        i = 1
        for h in material.obtain:
            if i != 1:
                obtain += '\n'
            obtain += f'\u2022 {h}'
            i += 1

        embed = discord.Embed(title=f'{material.name}', description=f'{desc}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(name='How to Obtain', value=obtain, inline=False)
        embed.set_footer(text=f'Type: {material.type}')
        return embed