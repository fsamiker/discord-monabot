from discord.ext.commands.errors import UserInputError
from bot.utils.embeds import send_game_embed_misc
from bot.utils.queries.minigame_queries import query_top_ten_players, query_top_ten_players_in_guild
from datetime import datetime, timedelta
from bot.utils.queries.genshin_database_queries import query_random_boss, query_total_players
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import discord
import random

class Leaderboards(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx, option:str='guild'):
        """Check genshin minigame leaderboards"""

        if option.lower() not in ['global', 'guild']:
            raise UserInputError

        if option.lower() == 'global':
            title = 'Leaderboard - Global'
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                users = await s.run_sync(query_top_ten_players)
                if not users:
                    await send_game_embed_misc(ctx, title, f"There doesn't seem to be any players")
                else:
                    embed = self.build_leader_embed(title, users)
                    await ctx.send(embed=embed)
        elif option.lower() == 'guild':
            title = f'Leaderboard - Guild ({ctx.guild.name})'
            async with AsyncSession(self.bot.get_cog('Query').engine) as s:
                guild_members = [m.id for m in ctx.guild.members]
                users = await s.run_sync(query_top_ten_players_in_guild, guild_members=guild_members)
                if not users:
                    await send_game_embed_misc(ctx, title, f"There doesn't seem to be any players")
                else:
                    embed = self.build_leader_embed(title, users)
                    await ctx.send(embed=embed)


    def build_leader_embed(self, title, users):
        embed = discord.Embed(title=title, color=discord.Colour.purple())
        desc = ''
        i = 1
        for p in users:
            user = self.bot.get_user(p.discord_id)
            if user is None:
                continue
            desc += f'`{i:02}.`: {self.bot.get_cog("Flair").get_emoji("AR")}{p.level} - **{user.display_name}**\n'
            i += 1
        embed.description = desc
        return embed