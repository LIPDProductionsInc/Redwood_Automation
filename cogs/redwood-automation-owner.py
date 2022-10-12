import discord
import aiohttp
import asyncio
import datetime
import json
import psutil
import sys
import traceback

from discord.ext import commands

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
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
        else:
            await ctx.send(f'**`Cog: {cog} has loaded successfully`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
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
        else:
            print(f'{cog} has unloaded successfully!')
            await ctx.send(f'**`Successfuly unloaded Cog: {cog}`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog: str):
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
        else:
            await ctx.send(f'**`Successfully loaded {cog}`**')
            print(f'Cog: {cog} has loaded sucessfuly!')
            pass
        pass

    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def _sync(self, ctx) -> None:
        await ctx.send('`Syncing Slash commands...`')
        print('Syncing slash commands')
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"`Synced {len(synced)} commands`")
        print(f"Synced {len(synced)} commands")
        return

    
    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
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
    async def _rules(self, ctx):
        channel = self.bot.get_channel(646541638763544586)
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
        embed.set_footer(text='Rules lase updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass

    @commands.command(name='info', hidden=True)
    @commands.is_owner()
    async def _info(self, ctx):
        channel = self.bot.get_channel(646541638763544586)
        await ctx.message.delete()
        embed = discord.Embed(
            colour=discord.Color.dark_blue(),
            description='[Server Invite](https://discord.gg/Kf9T6h2) \n [ROBLOX Group](https://www.roblox.com/groups/4017784/City-of-Redwood)'
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/646552474265845780/1028765111411810305/Capture4.PNG")
        embed.set_author(name='Redwood Information')
        embed.add_field(name='Council Boards', value='[City Council](https://trello.com/b/gVPTVd0r) \n [City Records](https://trello.com/b/g06YwcHJ)', inline=False)
        embed.add_field(name='Administration Boards', value='[Office of the Mayor](https://trello.com/b/pK66sdV7) \n [Office of Commerce Relations](https://trello.com/b/ePQVqR70)', inline=False)
        embed.add_field(name='Other Links', value='[City Charter](https://trello.com/c/T3jW7f8m) \n [Floor Rules](https://trello.com/c/XpLJXTTI) \n [Twitter](http://twitter.com/CityofRedwood)', inline=False)
        embed.set_footer(text='Information last updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass
    
    @commands.command(name='edit', hidden=True)
    @commands.is_owner()
    async def _edit(self, ctx, id, content):
        message = await channel.fetch_message(id)
        await message.edit(content=content)
        pass
    
    @commands.command(name='stats', hidden=True)
    @commands.is_owner()
    async def _stats(self, ctx):
        embed = discord.Embed(
            title='Redwood Deli',
            type='rich',
            colour=discord.Color(0xFF9E00),
            description=f'''
Python Version: **{sys.version}**

Discord.py Version: **{discord.__version__}**

Current CPU Usage: **{psutil.cpu_percent()}**

Current RAM Usage: **{psutil.virtual_memory().percent}**

Average System Load: **{[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]}%**

Latency: **{round(self.bot.latency * 1000)}**ms
'''
            )
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name='role-request', hidden=True)
    @commands.is_owner()
    async def _rolerequest(self, ctx):
        request_role = """
The following roles can be requested from <@155149108183695360> using `?rank` followed by the name of the role:
- <@&1000334009651429467>
- <@&1001014065822453800>
- <@&1001013976840294450>
        """
        notice = """
- Your up-to-date callsign or rank **MUST** be a part of your nickname
- Applicants, Candidates, Probationary Officers, etc., do **NOT** get department roles
        """
        embed = discord.Embed(
            title="**ROLE REQUEST**",
            colour=discord.Color.blue(),
            description="""
To be able to view all the necessary channels in this server, you must have the appropriate role(s).

If you have verified with <@426537812993638400> before, check your DM's, because most likely your roles have already been given to you.
If you have not verified with <@426537812993638400> before, run `/verify` and make sure to select the command from <@426537812993638400> to get yourself verified.
If you still have not gotten all the roles you need, open a <#999293384504119326> to request the roles you need. **ANY REQUESTS MADE IN THIS CHANNEL WILL NOT BE SEEN!!!**

If you need new roles, first run `/update` from <@426537812993638400> to get your roles updated, if that fails, open a <#999293384504119326>."""
        )
        embed.add_field(name='**Requestable Roles**', value=request_role, inline=True)
        embed.add_field(name='**Notice to Department Employees:**', value=notice, inline=True)
        embed.set_footer(text=f"Developed by {self.bot.owner}", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot):
