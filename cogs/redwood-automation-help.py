from unicodedata import name
import discord
import datetime

from discord.ext import commands
from datetime import timedelta

class HelpCog(commands.Cog, name="Help Cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        if command is None:
            embed = discord.Embed(title="Help", description="Here's a list of all my commands:", color=0x00ff00)
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if cog.qualified_name == "Owner Cog":
                    continue
                if cog.qualified_name == "Help Cog":
                    continue
                if cog.qualified_name == "Error Cog":
                    continue
                if cog.qualified_name == "Admin Cog":
                    continue
                if cog.qualified_name == "Commands Cog":
                    continue
                embed.add_field(name=cog.qualified_name, value="`" + "`, `".join([c.name for c in cog.get_commands()]) + "`", inline=False)
            embed.set_footer(text="Use !help <command> for more info on a command.")
            await ctx.send(embed=embed)
        else:
            if (cmd := self.bot.get_command(command)) is not None:
                embed = discord.Embed(title=f"Help for {cmd.name}", description=cmd.help, color=0x00ff00)
                embed.add_field(name="Usage", value=f"`{cmd.signature}`", inline=False)
                if cmd.aliases:
                    embed.add_field(name="Aliases", value="`" + "`, `".join(cmd.aliases) + "`", inline=False)
                if isinstance(cmd, commands.Command):
                    embed.add_field(name="Cooldown", value=cmd._buckets._cooldown.per, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("That command doesn't exist.")
                pass
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(HelpCog(bot))