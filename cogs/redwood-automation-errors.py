import discord
import requests
import roblox
import sqlite3
import sys
import traceback

from discord.ext import commands, tasks
from roblox import InternalServerError

class CommandErrorHandler(commands.Cog, name="Command Error Handler"):

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
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            print('Unknown command sent')
            await ctx.send(':x: | I do not know that command. `!help` has a list of commands that can be used.')

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
            
        elif isinstance(error, commands.NotOwner):
            await ctx.send(':x: | This command is restricted to the owner only.')
            
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(':x: | Argument needed')
            
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send(':x: | <@!222766150767869952> That cog is already loaded')
            
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(':x: | <@!222766150767869952> Could not load cog. Check the terminal for more details')
            
        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send(':x: | <@!222766150767869952> Cog failed. Check the terminal for more details')
            
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(':x: | <@!222766150767869952> Could not find cog. Check the spelling and try again')
            
        elif isinstance(error, commands.CommandRegistrationError):
            await ctx.send(':x: | <@!222766150767869952> Command is already in service. Check the spelling and try again')
            
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(':x: | My perms got disabled. Please tag someone who can help! (Missing {error.missing_perms})')
            
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f':x: | You need the {error.missing_perms} permission to run this command!')
            
        elif isinstance(error, commands.MissingRole):
            await ctx.send(f'This command is restricted to {error.missing_role}s only!')

        elif isinstance(error, commands.MissingAnyRole):
            if ctx.command.qualified_name == 'accept':
                await ctx.send(f':x: | This command can only be used by management')
            else:
                await ctx.send(f':x: | This command can only be used by {error.missing_roles}')
            
        elif isinstance(error, ZeroDivisionError):
            await ctx.send('Cannot divide by zero!')
            
        elif isinstance(error, AttributeError):
            await ctx.send(f':x: | AttributeError: {error}')
            
        elif isinstance(error, NameError):
            await ctx.send(f':x: | NameError: {error}')
        
        elif isinstance(error, ValueError):
            await ctx.send(f':x: | ValueError: {error}')
        
        elif isinstance(error, SyntaxError):
            await ctx.send(f':x: | SyntaxError: {error}')
            
        elif isinstance(error, KeyError):
            await ctx.send(f':x: | KeyError: {error} is not found')
            
        elif isinstance(error, TypeError):
            await ctx.send(f':x: | TypeError: {error}')
        
        elif isinstance(error, IndexError):
            await ctx.send(f':x: | IndexError: {error}')
            
        elif isinstance(error, discord.HTTPException):
             await ctx.send(f':x: | HTTPException: {error.status} (error code: {error.code}): {error.text}')
        
#         if isinstance(error, requests.RequestsException):
#             await ctx.send(':x: | There was an ambiguous exception that occurred while trying to fetch the API data.')
#             
#         if isinstance(error, requests.ConnectionError):
#             await ctx.send(':x: | Could not connect to the API.')
#             
#         if isinstance(error, requests.HTTPError):
#             await ctx.send(':x: | An HTTP error occurred.')
#         
#         if isinstance(error, requests.URLRequired):
#             await ctx.send(':x: | Uhhhh, <@222766150767869952> you deleted the URL...')
#             
#         if isinstance(error, requests.TooManyRedirects):
#             await ctx.send(':x: | API has too many redirects.')
#             
#         if isinstance(error, requests.ConnectTimeout):
#             await ctx.send(':x: | The request timed out while trying to connect to the API.')
#             
#         if isinstance(error, requests.ReadTimeout):
#             await ctx.send(':x: | API didn\'t respond in time. Please try again.')
#         
#         if isinstance(error, requests.Timeout):
#             await ctx.send(':x: | The request timed out. Please try again.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
            
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(':x: | Error not captured')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        else:
            exc_type, exc_value, exc_tb = sys.exc_info()
            new_line = '\n'
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
#            await channel.send(f':x: | ERROR IN r!{ctx.command}: {f"{new_line}".join(traceback.format_exception(exc_type, exc_value, exc_tb))}')

    @commands.command(name='repeat', aliases=['mimic', 'copy'])
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")


async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))