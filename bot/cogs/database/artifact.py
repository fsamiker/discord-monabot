from bot.utils.checks import has_args
from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Artifact
from data.db import session_scope
from  sqlalchemy.sql.expression import func
from discord.ext import commands
import discord

class Artifacts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def artifact(self, ctx, *args):
        """Get Artifact Set Details"""

        async def usage(message):
            examples = '''```Command: artifact <artifact name>

Example Usage:
\u2022 m!artifact gladiator's finale
\u2022 m!artifact berserker```'''
            await ctx.send(f'{message}\n{examples}')

        if not args:
            raise commands.UserInputError

        name = ' '.join([w.capitalize() for w in args])
        with session_scope() as s:
            art = s.query(Artifact).filter(Artifact.name.like(f'%{name}%')).first()
            if art:
                file = discord.File(art.icon_url, filename='image.png')
                embed = self.get_set_info_embed(art)
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send(f'Could not find material "{name}"')

    def get_set_info_embed(self, art):
        embed = discord.Embed(title=f'{art.name} Set', color=discord.Colour.gold())
        embed.set_thumbnail(url='attachment://image.png')

        min_rar = ''
        max_rar = ''
        if art.min_rarity:
            for _ in range(art.min_rarity):
                min_rar += f'{self.bot.get_cog("Flair").get_emoji("Star")}'
        if art.max_rarity:
            for _ in range(art.max_rarity):
                max_rar += f'{self.bot.get_cog("Flair").get_emoji("Star")}'

        if min_rar and max_rar:
            embed.description = f'Min Rarity: {min_rar}\nMax Rarity: {max_rar}'
        elif min_rar:
            embed.description = f'Rarity: {min_rar}\n'

        if art.domains:
            dom_name = []
            for d in art.domains:
                if d.domain.name not in dom_name:
                    dom_name.append(d.domain.name)
            dom = '\u2022 '
            dom += '\n\u2022 '.join(dom_name)
            embed.add_field(name='Domains Dropped', value=dom, inline=False)

        if art.bonus_one:
            embed.add_field(name='1-Set Bonus', value=art.bonus_one, inline=False)
        if art.bonus_two:
            embed.add_field(name='2-Set Bonus', value=art.bonus_two, inline=False)
        if art.bonus_three:
            embed.add_field(name='3-Set Bonus', value=art.bonus_three, inline=False)
        if art.bonus_four:
            embed.add_field(name='4-Set Bonus', value=art.bonus_four, inline=False)
        if art.bonus_five:
            embed.add_field(name='5-Set Bonus', value=art.bonus_five, inline=False)
        
        return embed