from discord.ext.commands.cooldowns import BucketType
from data.genshin.models import Domain, DomainLevel
from data.db import session_scope
from  sqlalchemy.sql.expression import func
from sqlalchemy import or_
from discord.ext import commands
from datetime import datetime
import discord

class Domains(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(5, BucketType.guild, wait=True)
    async def domain(self, ctx, *args):
        """Get Domain Details"""

        async def usage(message):
            examples = '''```Command: domain <domain name> optional: <level> <day of the week>
\u2022 level : Domain Floor Level (Default: Max Level)
\u2022 day of the week : Day of the week (Default: Sunday for domains dependant on days) 

Example Usage:
\u2022 m!domain Midsummer Courtyard
\u2022 m!domain forsaken rift 3
\u2022 m!domain ceceilia garden 3 monday```'''
            await ctx.send(f'{message}\n{examples}')

        if ctx.guild:
            server_region = ctx.guild.region.name
        else:
            server_region = 'GMT'

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
        with session_scope() as s:
            dom = s.query(Domain).filter(Domain.name.ilike(f'%{name}%')).first()
            if not dom:
                await ctx.send(f'Could not find Domain "{name}"')
                return
            if lvl and day:
                domlvl = s.query(DomainLevel).filter(DomainLevel.domain_id==dom.id, DomainLevel.level==lvl, or_(DomainLevel.day==day, DomainLevel.day==None)).first()
            elif lvl > 0:
                domlvl = s.query(DomainLevel).filter(DomainLevel.domain_id==dom.id, DomainLevel.level==lvl, or_(DomainLevel.day=='Sunday', DomainLevel.day==None)).first()
            elif day:
                domlvl = s.query(DomainLevel).filter(DomainLevel.domain_id==dom.id, or_(DomainLevel.day==day, DomainLevel.day==None)).order_by(DomainLevel.level.desc()).first()
            else:
                domlvl = s.query(DomainLevel).filter(DomainLevel.domain_id==dom.id, or_(DomainLevel.day=='Sunday', DomainLevel.day==None)).order_by(DomainLevel.level.desc()).first()
            if domlvl:
                file = discord.File(dom.icon_url, filename='image.png')
                embed = self.get_domain_info_embed(domlvl)
                await ctx.send(file=file, embed=embed)
            else:
                error = f'Could not find Domain "{name}"'
                if lvl:
                    error += f' Floor Lvl {lvl}'
                if day:
                    error += f' - {lvl}'
                await ctx.send(error)

        
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