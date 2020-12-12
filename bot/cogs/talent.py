from bot.utils.text import get_texttable
from discord.ext import commands
import discord

class Talent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.talents = self.bot.get_cog('Character').skills

    @commands.command()
    async def talent(self, ctx, *args):
        """Get Talent Details"""

        async def usage(message):
            examples = '''```Command: talent <talent name>

Example Usage:
\u2022 m! talent sharpshooter
\u2022 m! talent Kaboom!```'''
            await ctx.send(f'{message}\n{examples}')

        if any([type(w)!=str for w in args]):
            await usage('Invalid command')
            return

        talent_name = ' '.join([w.capitalize() for w in args])
        if talent_name not in self.talents.keys():
            await ctx.send(f'Could not find talent "{talent_name}"')

        talent = self.talents.get(talent_name)
        file = discord.File(talent.get_icon(), filename='image.png')
        embed = self.get_talent_basic_info_embed(talent)
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def talentstats(self, ctx, *args):
        """Get Talent Details"""

        async def usage(message):
            examples = '''```Command: talentstats <talent name>

Example Usage:
\u2022 m! talentstats sharpshooter
\u2022 m! talentstas Kaboom!```'''
            await ctx.send(f'{message}\n{examples}')

        if any([type(w)!=str for w in args]):
            await usage('Invalid command')
            return

        talent_name = ' '.join([w.capitalize() for w in args])
        if talent_name not in self.talents.keys():
            await ctx.send(f'Could not find talent "{talent_name}"')

        talent = self.talents.get(talent_name)
        file = discord.File(talent.get_icon(), filename='image.png')
        embed = self.get_talent_stats_embed(talent)
        await ctx.send(file=file, embed=embed)



    def get_talent_basic_info_embed(self, talent):
        emojis = self.bot.get_cog('Emoji').emojis
        embed = discord.Embed(title=f'{talent.name}', description=f'{talent.description}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=f'{talent.type}')
        return embed

    def get_talent_stats_embed(self, talent):
        emojis = self.bot.get_cog('Emoji').emojis
        stats = f'{talent.name} is a Passive Talent'
        if talent.scaling:
            values = [list(r.values()) for r in talent.scaling]
            stats = get_texttable(list(talent.scaling[0].keys()), values)
        print(stats.draw())
        print(len(stats.draw()))
        embed = discord.Embed(title=f'{talent.name}', description=f'{stats.draw()}')
        embed.set_thumbnail(url='attachment://image.png')
        embed.set_footer(text=f'{talent.type}')
        return embed