import discord
import aiohttp
import asyncio
import datetime
import json
import psutil
import roblox
import sys
import traceback
import os

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from roblox import Client
from typing import Literal

load_dotenv()
client = Client(os.getenv("RobloxToken"))

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx:commands.Context, *, cog:str) -> None:
        await ctx.send(f'**`Loading Cog: {cog}...`**')
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Loading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await asyncio.sleep(2)
            await self.bot.load_extension(f'cogs.redwood-automation-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in loading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            await ctx.send(f'**`Cog: {cog} has loaded successfully`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx:commands.Context, *, cog:str) -> None:
        await ctx.send(f'**`Unloading Cog: {cog}...`**')
        await asyncio.sleep(2)
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Unloading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await self.bot.unload_extension(f'cogs.redwood-automation-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in unloading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            print(f'{cog} has unloaded successfully!')
            await ctx.send(f'**`Successfuly unloaded Cog: {cog}`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx:commands.Context, *, cog:str) -> None:
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        print('Reloading cog...')
        await asyncio.sleep(0.1)
        print('Cog Name:')
        await asyncio.sleep(0.1)
        print(cog)
        try:
            await ctx.send(f'**`Unloading Cog: {cog}...`**')
            await self.bot.unload_extension(f'cogs.redwood-automation-{cog}')
            await asyncio.sleep(2)
            await ctx.send(f'**`Loading Cog: {cog}...`**')
            await self.bot.load_extension(f'cogs.redwood-automation-{cog}')
            await asyncio.sleep(1)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in reloading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            await ctx.send(f'**`Successfully loaded {cog}`**')
            print(f'Cog: {cog} has loaded sucessfuly!')
            pass
        pass

    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def _sync(self, ctx:commands.Context) -> None:
        await ctx.send('`Syncing Slash commands...`')
        print('Syncing slash commands')
        synced = await ctx.bot.tree.sync()
        city_synced = await ctx.bot.tree.sync(guild=discord.Object(1150770058847588492))
        pd_synced = await ctx.bot.tree.sync(guild=discord.Object(1005182438265335901))
        await ctx.send(f"`Synced {len(synced)} commands globally, {len(city_synced)} commands in the City of Redwood guild, and {len(pd_synced)} commands in the Redwood Police Department guild`")
        print(f"Synced {len(synced)} commands globally, {len(city_synced)} commands in the City of Redwood guild, and {len(pd_synced)} commands in the Redwood Police Department guild")
        return

    
    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx:commands.Context, *, body:str) -> None:
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
                pass
            pass
        pass
    
    @commands.command(name='rules', hidden=True)
    @commands.is_owner()
    async def _rules(self, ctx:commands.Context) -> None:
        channel = self.bot.get_channel(1150770059418022001)
        await ctx.message.delete()
        embed = discord.Embed(
            colour=discord.Colour.dark_blue(),
            description='Welcome to the City of Redwood discord server. Please read & abide by our server rules at all times.'
            )
        embed.set_author(name='City of Redwood Rules', icon_url='https://cdn.discordapp.com/attachments/646552474265845780/1028765111411810305/Capture4.PNG')
        embed.add_field(name='1. Your server nickname should be set to your full Roblox username', value='No abbreviations or special characters should be included. Your nickname must be clearly visible. Callsigns are allowed to be included.', inline=False)
        embed.add_field(name='2. Be respectful to everyone in the server', value='Treat others how you would want to be treated', inline=False)
        embed.add_field(name='3. Spamming is strictly forbidden', value='This includes mention spamming, text spamming, et cetera', inline=False)
        embed.add_field(name='4. NSFW (Not Safe for Work) is strictly forbidden', value='This includes gore, pornography, and relevant content', inline=False)
        embed.add_field(name='5. Targetting someone in any means is strictly forbidden', value='You will not find a place in this Discord server should you break this rule', inline=False)
        embed.add_field(name='6. Any type of malicious links, files, or anything of the sort, are strictly forbidden', value='Violating this rule will result in your permanent removal from this server', inline=False)
        embed.add_field(name='7. Do not argue in any public text channel', value='If you wish to argue, take it to direct messages', inline=False)
        embed.add_field(name='8. Utilize appropriate profile pictures', value='They may not consist of pornography, gore, or have relations to a terrorist organization', inline=False)
        embed.set_footer(text='Rules last updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass

    @commands.command(name='info', hidden=True)
    @commands.is_owner()
    async def _info(self, ctx:commands.Context) -> None:
        channel = self.bot.get_channel(1150770059418022001)
        await ctx.message.delete()
        embed = discord.Embed(
            colour=discord.Color.dark_blue(),
            description='[Server Invite](https://discord.gg/Kf9T6h2) \n [ROBLOX Group](https://www.roblox.com/groups/4017784/City-of-Redwood)'
        )
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        embed.set_author(name='Redwood Information')
        embed.add_field(name='Council Boards', value='[City Council](https://trello.com/b/gVPTVd0r)\n[City Records](https://trello.com/b/g06YwcHJ)', inline=False)
        embed.add_field(name='Administration Boards', value='[Office of the Mayor](https://trello.com/b/F59t3HaG/) \n[Office of Commerce Relations](https://trello.com/b/ePQVqR70)', inline=False)
        embed.add_field(name='Other Links', value='[City Charter](https://trello.com/c/Pm1y1ZzD) \n[Floor Rules](https://trello.com/c/XpLJXTTI) \n[Twitter](http://twitter.com/CityofRedwood) \n[RPD Handbook](https://docs.google.com/document/d/18K-IHoT6MStN6b_kb7RSBGEpxMuSYgepN21Fw4TFtR0/edit) \n[RPD Public Database](https://docs.google.com/spreadsheets/d/1y5Cgqdn9faUx_nLvaO7RT6V93ehXzMTv68Q00OAOcoo/edit)', inline=False)
        embed.set_footer(text='Information last updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass
    
    @commands.command(name='edit', hidden=True)
    @commands.is_owner()
    async def _edit(self, ctx:commands.Context, id:int, content:str) -> None:
        message = await ctx.fetch_message(id)
        await message.edit(content=content)
        pass

    @commands.command(name='edit-specific', hidden=True)
    @commands.is_owner()
    async def _edit_specific(self, ctx:commands.Context, type:str = None) -> None:
        if type == None:
            await ctx.send('Please specify a type', ephemeral=True)
        elif type == 'role-request':
            message = await ctx.fetch_message(1038828402536349736)
            embed = message.embeds[0]
            embed.set_field_at(0, name='Requestable Roles', value='The following roles can be requested: \n- <@&763478824641495040> \n- <@&959865461846204436> \n- <@&853817144243650561> \n- <@&1024429857104478228> \n- <@&1045827799967088840> \n- <@&1097402926143655977>', inline=True)
            embed.set_field_at(2, name='Notice to Business Owners:', value='To get the <@&762321175900454933> role, fill out the `/business-represenantive` command', inline=False)
            embed.set_footer(text=f'Developed by {self.bot.owner}')
            embed.set_thumbnail(url=str(self.bot.user.avatar))
            await message.edit(embed=embed)
        elif type == 'information-links':
            message = await ctx.fetch_message(1154243793869090917)
            embed = message.embeds[0]
            embed.set_field_at(1, name='Administration Boards', value='[Office of the Mayor](https://trello.com/b/F59t3HaG/) \n[Office of Commerce Relations](https://trello.com/b/ePQVqR70)', inline=False)
            embed.set_thumbnail(url=str(self.bot.user.avatar))
            embed.timestamp = datetime.datetime.now()
            await message.edit(embed=embed)
            pass
    
    @commands.command(name='stats', hidden=True)
    @commands.is_owner()
    async def _stats(self, ctx:commands.Context) -> None:
        embed = discord.Embed(
            title='Redwood Automation',
            type='rich',
            colour=discord.Color.dark_blue(),
            description=f'''
Python Version: **{sys.version}**

Discord.py Version: **{discord.__version__}**

Current CPU Usage: **{psutil.cpu_percent()}**%

Current RAM Usage: **{psutil.virtual_memory().percent}**%

Average System Load: **{[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]}%**

Latency: **{round(self.bot.latency * 1000)}**ms
'''
            )
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name='restart', hidden=True)
    @commands.is_owner()
    async def _restart(self, ctx:commands.Context) -> None:
        await ctx.send('Restarting...')
        await self.bot.logout()
        pass

    @commands.command(name='verify', hidden=True)
    @commands.is_owner()
    async def _verify(self, ctx:commands.Context) -> None:
        embed = discord.Embed(
            title='Verification Needed',
            type='rich',
            colour=discord.Color.dark_blue(),
            description='If you are seeing this message, you have not verified your account. Please verify your account by typing `/verify` in <#646550331991523328>.'
        )
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name='role-request', hidden=True)
    @commands.is_owner()
    async def _rolerequest(self, ctx:commands.Context) -> None:
        request_role = """
The following roles can be requested:
- <@&1150770058897920153>
- <@&1150770058897920150>
- <@&1150770058881155123>
- <@&1150770058881155122>
- <@&1150770058847588495>
- <@&1150770058847588494>
        """
        notice = """
- Your up-to-date callsign or rank **MUST** be a part of your nickname
        """
        businesses = """
To get the <@&1150770058868568108> role, fill out the `/business-represenantive` command. Please include the link to your business permit from FDOCM
        """
        embed = discord.Embed(
            title="**ROLE REQUEST**",
            colour=discord.Color.blue(),
            description="""
Most roles are managed through <@426537812993638400> and can be given using `/verify` or `/update`.
The roles that are requestable are listed below and require you to ping <@&1150770058914705535> to get them."""
        )
        embed.add_field(name='**Requestable Roles**', value=request_role, inline=True)
        embed.add_field(name='**Notice to Department Employees:**', value=notice, inline=True)
        embed.add_field(name='**Notice to Business Owners:**', value=businesses, inline=True)
        embed.set_footer(text=f"Developed by {self.bot.owner}", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(OwnerCog(bot))
