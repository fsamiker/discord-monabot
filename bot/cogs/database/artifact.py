from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Artifact, DomainLevel
from discord.ext import commands
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import discord

def query_artifact(session, name):
    stmt = select(Artifact).options(selectinload(Artifact.domains).selectinload(DomainLevel.domain)).filter(Artifact.name.like(f'%{name}%'))
    art = session.execute(stmt).scalars().first()
    return art

class Artifacts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def artifact(self, ctx, *args):
        """Get Artifact Set Details"""
        if not args:
            raise commands.UserInputError

        name = ' '.join([w.capitalize() for w in args])
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            art = await s.run_sync(query_artifact, name=name)
            if art:
                file = discord.File(art.icon_url, filename='image.png')
                embed = self.get_set_info_embed(art)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

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