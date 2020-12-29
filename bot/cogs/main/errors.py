from bot.utils.error import NoResultError, ResinError
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import traceback
import sys

import sqlalchemy

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

        if isinstance(error, ResinError):
            await self.send_error_embed(ctx, f"Resin Value Error",
             description=f"Invalid Resin Value.\nResin value should be a number and not > 160\n"
                         f"Please use `{self.bot.command_prefix}help {ctx.command}` "
                         f"for command details")
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await self.send_error_embed(ctx, f"Missing Permissions Error", '**{}** permission(s) needed to run `{}` command.'.format(fmt, ctx.command))
            return

        if isinstance(error, commands.CommandOnCooldown) or isinstance(error, commands.MaxConcurrencyReached):
            await self.send_error_embed(ctx, 'Server is Busy', f"Due to server load, cooldown has been applied.\nTry again in a little while")
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            await self.send_error_embed(ctx, f"Missing Permissions Error", '**{}** permission(s) needed to run `{}` command.'.format(fmt, ctx.command))
            return

        if isinstance(error, discord.errors.Forbidden):
            permissions = ['View Channel', 'Send Messages', 'Embed Links', 'Attach Files', 'Add Reactions', 'Use External Emoji', 'Mention roles', 'Manage Messages', 'Read Message History']
            p_list = '\u2022 '+ '\n\u2022 '.join(permissions)
            msg = f'It seems mona is missing some permissions for full functionality\n\nKindly check that the following permissions are granted:\n{p_list}'
            msg += f'\n\nRest assured these permissions are to provide a richer experience such as better response UI using embeds and paginated pages with reaction management'
            msg += f"\n\n[How to add permission](https://support.discord.com/hc/en-us/articles/206029707-How-do-I-set-up-Permissions-#:~:text=Assigning%20Roles&text=Click%20on%20the%20'Members'%20tab,you%20assigned%20to%20that%20role.)"
            await self.send_error_embed(ctx, f"Missing Permissions Error", msg)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await self.send_error_embed(ctx, f"Command Error", f" `{ctx.command}` command cannot be used in direct messages")
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.UserInputError):
            await self.send_error_embed(ctx, f"Command Error",
             description=f"Invalid user input.\n"
                         f"Please use `{self.bot.command_prefix}help {ctx.command}` "
                         f"for command details")
            return

        if isinstance(error, NoResultError):
            await self.send_error_embed(ctx, f"No Results", f"Could not find results for\n`{ctx.message.content}`")
            return

        if isinstance(error, commands.DisabledCommand):
            await self.send_error_embed(ctx, f"Disabled Command", "Command is temporarily unavailable at the moment")
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await self.send_error_embed(ctx, f"Command Error", f" `{ctx.command}` command cannot be used in private messages")
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await self.send_error_embed(ctx, "Invalid Member", "Could not find tagged member in channel")
            else:
                await self.send_error_embed(
                    ctx,
                    f"Command Error",
                    description=f"Invalid user input.\n"
                                f"Please use `{self.bot.command_prefix}help {ctx.command}` "
                                f"for command details")
                return

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            traceback.print_exception(type(error), error, error.__traceback__, file=None)
            pass

    async def send_error_embed(self, ctx, title, description):
        embed = discord.Embed(title=title,
        description=description,
        color=discord.Color.red())
        file=discord.File('assets/genshin/icons/i_unimpressed_paimon.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(embed=embed, file=file)