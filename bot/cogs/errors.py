from datetime import datetime, timedelta
import discord
from discord.ext import commands
import traceback
import sys

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if isinstance(error, commands.CommandNotFound):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)


        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            embed = discord.Embed(title=f"{ctx.command} error",
                                description='I need the **{}** permission(s) to run this command.'.format(fmt),
                                color=discord.Color.red())
            embed.set_footer(text=f"{error}")
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.CommandOnCooldown) or isinstance(error, commands.MaxConcurrencyReached):
            embed = discord.Embed(description=f"Due to server load, cooldown has been applied.\nTry again in a little while",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"{_message}",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(title=f"{ctx.command} error",
                                    description="This command cannot be used in direct messages",
                                    color=discord.Color.red())
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.UserInputError) or isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title=f"Command error",
                                description=f"Invalid user input. "
                                            f"Please use `{self.bot.command_prefix}help {ctx.command}` "
                                            f"for command details",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')
            else:
                embed = discord.Embed(title=f"Command error",
                                description=f"Invalid user input. "
                                            f"Please use `{self.bot.command_prefix}help {ctx.command}` "
                                            f"for command details",
                                color=discord.Color.red())
                await ctx.send(embed=embed)
                return

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            traceback.print_exception(type(error), error, error.__traceback__, file=None)
            pass