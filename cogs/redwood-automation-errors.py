import discord
import datetime
import requests
import roblox
import sqlite3
import sys
import traceback

from discord.ext import commands
from discord.app_commands import AppCommandError
from roblox import InternalServerError

class CommandErrorHandler(commands.Cog, name="Command Error Handler"):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    def cog_load(self) -> None:
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error) -> None:
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
            if ctx.message.content.startswith('??') or ctx.message.content.startswith('!!') or ctx.message.content.startswith('?*') or ctx.message.content.startswith('!*'):
                return
            elif ctx.message.content.startswith('?mute') or ctx.message.content.startswith('?role'):
                await ctx.send('Why are you trying to trigger multiple bots? Use slash commands instead so you don\'t wake me up for no reason.')
            else:
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
            if ctx.command.qualified_name == 'city-ban' or ctx.command.qualified_name == 'city-unban':
                await ctx.send(':x: | You do not have permission to ban in either the City of Redwood\'s Discord server or RPD\'s Discord server.')
            else:
                await ctx.send(f':x: | You need the {error.missing_perms} permission to run this command!')
            
        elif isinstance(error, commands.MissingRole):
            if ctx.command.qualified_name == 'send':
                if error.missing_role == 1150770058914705528:
                    await ctx.send(':x: | Only the City Attorney can use this command!', ephemeral=True)
            else:
                await ctx.send(f'This command is restricted to {error.missing_role} only!')

        elif isinstance(error, commands.MissingAnyRole):
            if ctx.command.qualified_name == 'legal-review':
                await ctx.send(f':x: | This command can only be used by the City Council.', ephemeral=True)
            elif ctx.command.qualified_name == 'session':
                await ctx.send(f':x: | This command can only be used by the Presiding Officers.', ephemeral=True)
            elif ctx.command.qualified_name == 'end-session':
                await ctx.send(f':x: | This command can only be used by the Presiding Officers.', ephemeral=True)
            elif ctx.command.qualified_name == 'template':
                await ctx.send(f':x: | This command can only be used by the City Council.', ephemeral=True)
            elif ctx.command.qualified_name == 'send':
                await ctx.send(f':x: | This command can only be used by the City Attorney or the Presiding Officers.', ephemeral=True)
            elif ctx.command.qualified_name == 'floor':
                await ctx.send(f':x: | This command can only be used by the Presiding Officer.', ephemeral=True)
            elif ctx.command.qualified_name == 'dismiss':
                await ctx.send(f':x: | This command can only be used by the Presiding Officer.', ephemeral=True)
            elif ctx.command.qualified_name == 'propose':
                await ctx.send(f':x: | This command can only be used by the City Council.', ephemeral=True)
            elif ctx.command.qualified_name == 'transcript':
                await ctx.send(f':x: | This command can only be used by the Clerk\'s Office.', ephemeral=True)
            elif ctx.command.qualified_name == 'docket':
                await ctx.send(f':x: | This command can only be used by the Presiding Officers.', ephemeral=True)
            elif ctx.command.qualified_name == 'appoint':
                await ctx.send(f':x: | This command can only be used by the Mayor, Deputy Mayor or City Chairperson at this time.', ephemeral=True)
            elif ctx.command.qualified_name == 'elections':
                await ctx.send(f':x: | This command can only be used by the Mayor, Deputy Mayor or City Chairperson.', ephemeral=True)
            elif ctx.command.qualified_name == 'tweet':
                await ctx.send(f':x: | This command can only be used by the Press Secretary\'s Office.', ephemeral=True)
            elif ctx.command.qualified_name == 'applications':
                await ctx.send(f':x: | This command can only be used by the Police Chief.', ephemeral=True)
            elif ctx.command.qualified_name == 'oaths':
                await ctx.send(f':x: | This command can only be used by the County Executive, Mayor, Deputy Mayor, or Council Chairperson.', ephemeral=True)
            else:
                await ctx.send(f':x: | This command can only be used by {error.missing_roles}', ephemeral=True)
        
        elif isinstance(error, ZeroDivisionError):
            await ctx.send('Cannot divide by zero!')
            
        elif isinstance(error, AttributeError):
            await ctx.send(f':x: | AttributeError: {error}', ephemeral=True)
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            channel = ctx.bot.get_channel(784368117299150849)
            embed = discord.Embed(
                type='rich',
                colour = discord.Colour.red()
            )
            embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
            embed.add_field(name='Attribute Error', value=f'{error}', inline=False)
            embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
            embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
            embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
            embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
            embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
            
        elif isinstance(error, NameError):
            await ctx.send(f':x: | NameError: {error}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        elif isinstance(error, ValueError):
            await ctx.send(f':x: | ValueError: {error}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        elif isinstance(error, SyntaxError):
            await ctx.send(f':x: | SyntaxError: {error}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
        elif isinstance(error, KeyError):
            await ctx.send(f':x: | KeyError: {error} is not found')
            
        elif isinstance(error, TypeError):
            await ctx.send(f':x: | TypeError: {error}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        elif isinstance(error, IndexError):
            await ctx.send(f':x: | IndexError: {error}')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
        elif isinstance(error, discord.HTTPException):
            if error.status == 403 and error.code == 50013 and ctx.command.qualified_name == 'ban' or ctx.command.qualified_name == 'kick' or ctx.command.qualified_name == 'city-ban':
                prefix = await self.bot.get_prefix(ctx.message)
                await ctx.send(f'{ctx.author.mention} Yeah no, I ain\'t doing {prefix}{ctx.command.qualified_name} on {ctx.message.mentions[0].mention}.')
            else:
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
            elif ctx.command.qualified_name == "floor":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "legal-review":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "dimiss":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "send":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "propose":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "appoint":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "elections":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "tweet":
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == "applications":
                await ctx.send(error, ephemeral=True)
            else:
                await ctx.send(error, ephemeral=True)
                channel = ctx.bot.get_channel(784368117299150849)
                embed = discord.Embed(
                    type='rich',
                    colour = discord.Colour.red()
                )
                embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
                embed.add_field(name='Bad Argument Error', value=f'{error}', inline=False)
                embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
                embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
                embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
                embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
                embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
            
        elif isinstance(error, commands.CheckFailure):
            if ctx.command.qualified_name == 'transcript':
                await ctx.send('Only city clerks can create transcripts.', ephemeral=True)
            elif ctx.command.qualified_name == 'announce':
                await ctx.send('You do not have permission to announce.', ephemeral=True)
            elif ctx.command.qualified_name == 'issue':
                if ctx.guild.id == 1005182438265335901:
                    await ctx.send('This command cannot be used in this server.', ephemeral=True)
            else:
                await ctx.send(':x: | Error not captured', ephemeral=True)
                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
                channel = ctx.bot.get_channel(784368117299150849)
                embed = discord.Embed(
                    type='rich',
                    colour = discord.Colour.red()
                )
                embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
                embed.add_field(name='Check Failure Error', value=f'{error}', inline=False)
                embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
                embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
                embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
                embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
                embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)

        elif isinstance(error, commands.UserInputError):
            if ctx.command.qualified_name == 'floor':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'legal-review':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'propose':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'dimiss':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'end-session':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'docket':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'send':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'flip':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'roll':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'coin':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'dice':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'choose':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == '8ball':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'rps':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'rpsls':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'transcript':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'seal':
                await ctx.send(error, ephemeral=True)
            elif ctx.command.qualified_name == 'applications':
                await ctx.send(error, ephemeral=True)
            else:
                await ctx.send(':x: | UserInputError: {}'.format(error), ephemeral=True)
                print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
                channel = ctx.bot.get_channel(784368117299150849)
                embed = discord.Embed(
                    type='rich',
                    colour = discord.Colour.red()
                )
                embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
                embed.add_field(name='User Input Error', value=f'{error}', inline=False)
                embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
                embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
                embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
                embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
                embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)

        elif isinstance(error, commands.CheckAnyFailure):
            if ctx.command.qualified_name == 'seal':
                await ctx.send("You can not change the seal.", ephemeral=True)
            else:
                await ctx.send("Error not captured. Sent to console for capturing", ephemeral=True)
                channel = ctx.bot.get_channel(784368117299150849)
                embed = discord.Embed(
                    type='rich',
                    colour = discord.Colour.red()
                )
                embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
                embed.add_field(name='Check Any Failure Error', value=f'{error}', inline=False)
                embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
                embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
                embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
                embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
                embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):
            channel = ctx.bot.get_channel(784368117299150849)
            embed = discord.Embed(
                type='rich',
                colour = discord.Colour.red()
            )
            embed.set_author(name='New Error', icon_url=str(ctx.bot.user.avatar))
            embed.add_field(name='Command Invoke Error', value=f'{error}', inline=False)
            embed.add_field(name='Command Ran', value=f'{ctx.command}', inline=False)
            embed.add_field(name='Guild', value=f'{ctx.guild}', inline=True)
            embed.add_field(name='Channel', value=f'{ctx.channel}', inline=True)
            embed.add_field(name='Message', value=f'{ctx.message.content}', inline=True)
            embed.set_footer(text=f'User ID: {ctx.author.id}', icon_url=str(ctx.author.avatar))
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
            await ctx.send(f"{error}", ephemeral=True)

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def on_app_command_error(self, interaction:discord.Interaction, error:AppCommandError):
        print('Ignoring exception in command {}:'.format(interaction.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='repeat', aliases=['mimic', 'copy'], hidden=True)
    async def do_repeat(self, ctx:commands.Context, *, inp: str) -> None:
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx:commands.Context, error) -> None:
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")


async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(CommandErrorHandler(bot))