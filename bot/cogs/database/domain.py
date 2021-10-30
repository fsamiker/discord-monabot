from bot.utils.error import NoResultError
from discord.ext.commands.cooldowns import BucketType
from sqlalchemy.exc import SQLAlchemyError
from data.genshin.models import Domain, DomainLevel
from sqlalchemy import or_
from discord.ext import commands
import discord
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

def query_domain(session, name):
    stmt = select(Domain).options(selectinload(Domain.levels)).filter(Domain.name.ilike(f'%{name}%'))
    dom = session.execute(stmt).scalars().first()
    return dom

def query_domainlvl(session, dom_id, lvl, day):
    if lvl and day:
        stmt = select(DomainLevel).options(selectinload(DomainLevel.material_drops), selectinload(DomainLevel.artifact_drops)).filter(DomainLevel.domain_id==dom_id, DomainLevel.level==lvl, or_(DomainLevel.day==day, DomainLevel.day==None))
    elif lvl > 0:
        stmt = select(DomainLevel).options(selectinload(DomainLevel.material_drops), selectinload(DomainLevel.artifact_drops)).filter(DomainLevel.domain_id==dom_id, DomainLevel.level==lvl, or_(DomainLevel.day=='Sunday', DomainLevel.day==None))
    elif day:
        stmt = select(DomainLevel).options(selectinload(DomainLevel.material_drops), selectinload(DomainLevel.artifact_drops)).filter(DomainLevel.domain_id==dom_id, or_(DomainLevel.day==day, DomainLevel.day==None)).order_by(DomainLevel.level.desc())
    else:
        stmt = select(DomainLevel).options(selectinload(DomainLevel.material_drops), selectinload(DomainLevel.artifact_drops)).filter(DomainLevel.domain_id==dom_id, or_(DomainLevel.day=='Sunday', DomainLevel.day==None)).order_by(DomainLevel.level.desc())
    domlvl = session.execute(stmt).scalars().first()
    return domlvl


class Domains(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def domain(self, ctx, *args):
        """Get Domain Details"""

        if not args:
            raise commands.UserInputError

        # Check Input
        lvl = 0
        name = ' '.join(args)
        if args[-1].lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = args[-1].capitalize()
            name = ' '.join(args[:-1])
            print(name)
            try:
                lvl = int(args[-2])
                name = ' '.join(args[:-2])
            except:
                pass
        else:
            day = None
            try:
                lvl = int(args[-1])
                name = ' '.join(args[:-1])
            except:
                pass
        
        name = name.title()
        async with AsyncSession(self.bot.get_cog('Query').engine) as s:
            dom = await s.run_sync(query_domain, name=name)
            if not dom:
                raise NoResultError
            domlvl = await s.run_sync(query_domainlvl, dom_id=dom.id, lvl=lvl, day=day)
            if domlvl:
                file = discord.File(dom.icon_url, filename='image.png')
                embed = self.get_domain_info_embed(domlvl)
                await ctx.send(file=file, embed=embed)
            else:
                raise NoResultError

        
    def get_domain_info_embed(self, domainlvl):
        flair = self.bot.get_cog("Flair")
        domain = domainlvl.domain
        title = f'{domain.name} Level: {domainlvl.level}'
        if domainlvl.day:
            title += f' ({domainlvl.day})'
        else:
            title += ' (All Days)'

        embed = discord.Embed(title=title, description=domain.description, color=discord.Colour.dark_gray())
        embed.set_image(url='attachment://image.png')

        embed.add_field(name=flair.get_emoji("AR"), value=domainlvl.ar_exp)
        embed.add_field(name=flair.get_emoji("FS"), value=domainlvl.friendship_exp)
        embed.add_field(name=flair.get_emoji("Mora"), value=domainlvl.mora)

        elements = domain.get_rec_elements()
        if elements:
            el = ''
            for e in elements:
                el+= f'{self.bot.get_cog("Flair").get_emoji(e)} '
            embed.add_field(name='Recommended Elements', value=el)
        embed.add_field(name='AR Requirement Level', value=domainlvl.requirement)

        if domainlvl.leyline:
            embed.add_field(name='Leyline', value=domainlvl.leyline, inline=False)
        else:
            embed.add_field(name='Leyline', value='No Leyline Effects', inline=False)

        if domainlvl.objective:
            embed.add_field(name='Objective', value=domainlvl.objective, inline=False)
        else:
            embed.add_field(name='Objective', value='N/A', inline=False)

        enemy_str = '\u2022 ' + '\n\u2022 '.join(domainlvl.get_enemies())
        embed.add_field(name='Enemies', value=enemy_str, inline=False)

        if domainlvl.material_drops:
            mats = [m.name for m in domainlvl.material_drops]
            mat_drop = '\u2022 '
            mat_drop += '\n\u2022 '.join(mats)
            embed.add_field(name='Possible Material Drops', value=mat_drop)

        if domainlvl.artifact_drops:
            arts = [f'{a.name} set pieces' for a in domainlvl.artifact_drops]
            art_drop = '\u2022 '
            art_drop += '\n\u2022 '.join(arts)
            embed.add_field(name='Possible Artifact Drops', value=art_drop)
        
        embed.set_footer(text=f'Location: {domain.location}, Type: {domain.typing}')
        return embed