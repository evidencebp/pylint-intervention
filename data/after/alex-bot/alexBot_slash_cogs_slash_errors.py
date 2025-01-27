import asyncio
import logging
import random
import traceback

import discord
from discord import Interaction
from discord.app_commands import AppCommandError
from discord.ext import commands

from ..tools import Cog

log = logging.getLogger(__name__)


class CommandErrorHandler(Cog):
    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    # -> Option 1 ---
    # detaching the handler when the cog is unloaded
    # this is optional for option 1
    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    # -> Option 1 ---
    # the global error handler for all app commands (slash & ctx menus)
    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError):
        log.error(f"app command error: {error} from {interaction.user} in {interaction.guild or 'DM'}")
        log.exception(error)
        if interaction.response.is_done():
            await interaction.followup.send(
                f"An Error Occurred while running this command. please contact {self.bot.owner.mention}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"An Error Occurred while running this command. please contact {self.bot.owner.mention}", ephemeral=True
            )

    @Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):

        error_messages = {str(commands.DisabledCommand): f'{ctx.command} has been disabled.'
                          , str(commands.NotOwner): f'{ctx.command} is a owner only command.'
                          , str(commands.NoPrivateMessage): f'{ctx.command} can not be used in Private Messages.'
                          , str(commands.CheckFailure): 'A Check failed for this command.'
                          , str(commands.MissingRequiredArgument): 
                            f'Parameter {error.param} is required but missing, See {ctx.prefix}help {ctx.command} for help!'
                          , str(commands.MissingPermissions): 'You do not have permission to run that command.'
                          }
        
        """The event triggered when an error is raised while invoking a command."""
        if isinstance(error, commands.CommandNotFound):
            return

        msg = None
        if isinstance(error, asyncio.TimeoutError):
            msg = f"timed out. you can start again with {ctx.prefix}{ctx.command}"

        msg = self._handle_load_errors(ctx, error, msg)

        if (isinstance(error, commands.DisabledCommand)
                or isinstance(error, commands.NotOwner)
                or isinstance(error, commands.NoPrivateMessage)
                or isinstance(error, commands.CheckFailure)
                or isinstance(error, commands.MissingRequiredArgument)
                or isinstance(error, commands.MissingPermissions)):
            msg = error_messages[str(error)]

        if isinstance(error, commands.BadArgument):
            ctx.command.reset_cooldown(ctx)
            msg = f'Bad argument: {error} See {ctx.prefix}help {ctx.command} for help!'
            log.warning(f"bad argument on {ctx.command}: {error}")

        error, msg = self._hadle_invoke_error(error)

        # post the error into the chat if no short error message could be generated
        if not msg:
            trace = traceback.format_exception(type(error), error, error.__traceback__, limit=5)
            actual_trace = '\n'.join(trace)
            msg = (
                f"Something, somewhere, broke. if {ctx.bot.owner.mention} isnt in this server, "
                f"so you'll have to join the server in `a!about`."
            )
            log.error(
                f"{ctx.author.id} broke bot running {ctx.command.cog_name}.{ctx.command.qualified_name}"
                f"\nquotable: {ctx.channel.id or 'DM'}-{ctx.message.id or None}\n"
                f":{actual_trace}"
            )

        allowed_mentions = discord.AllowedMentions(users=[ctx.bot.owner])

        try:
            await ctx.send(msg, allowed_mentions=allowed_mentions)
        except discord.HTTPException:
            await ctx.send('error message too long')

    def _handle_load_errors(self, ctx, error, msg):
        if isinstance(error, commands.MaxConcurrencyReached):
            if ctx.author.id == 335928292542513162 and random.random() < 0.2:
                msg = "DAWN PLS"
            else:
                msg = f"{ctx.command} is currently being ran. please wait for it to finish."

        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == 335928292542513162 and random.random() < 0.2:
                msg = "DAWN PLS"
            else:
                msg = f"{ctx.command} is being used too often, try again later"

        return msg

    def _hadle_invoke_error(self, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original

            if isinstance(error, discord.Forbidden):
                msg = (
                    'A permission error occurred while executing this command, '
                    'Make sure I have the required permissions and try again.'
                )
                
        return error,msg


async def setup(bot: commands.Bot):
    await bot.add_cog(CommandErrorHandler(bot))
