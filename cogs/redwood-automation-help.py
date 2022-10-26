import discord
import datetime

from discord.ext import commands
from datetime import timedelta

class HelpCog(commands.Cog, name="Help Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        embed = discord.Embed(
            title="Help",
            description="Here is a list of commands you can use with Redwood Automation.",
            color=discord.Color.dark_blue()
            )
        if discord.utils.get(ctx.author.roles, id=646549329493884929):
            embed.add_field(name="Council Commands", value="`propose`, `legal-review`, `charter`, `template`", inline=False)
        if discord.utils.get(ctx.author.roles, id=646549322682466305) or discord.utils.get(ctx.author.roles, id=646551227626160139) or discord.utils.get(ctx.author.roles, id=673008336010084378):
            embed.add_field(name="Presiding Officer Commands", value="`docket`, `session`, `end-session`, `floor`, `dismiss`, `send`", inline=False)
        if discord.utils.get(ctx.author.roles, id=646549330479546379):
            embed.add_field(name="City Attorney Commands", value="`send`", inline=False)
        embed.add_field(name="Commands", value="`help`, `ping`, `serverinfo`, `userinfo`, `avatar`, `council`", inline=False)
        embed.add_field(name="Moderation", value="`ban`, `kick`, `unban`", inline=False)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner}", icon_url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name="beta-help", description="Shows help about a command or the bot (Beta version)", aliases=["help-beta"], hidden=True)
    @commands.is_owner()
    async def help_beta(self, ctx, *, command: str = None):
        embed = discord.Embed(
        title="Help",
        description="Here is a list of commands you can use with Redwood Automation.",
        color=discord.Color.dark_blue()
        )
        if command is None:
            embed = discord.Embed(title="Help", description="Here's a list of all my commands:", color=0x00ff00)
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.kick_members:
                    if cog.qualified_name == "Admin Cog":
                        continue
                if discord.utils.get(ctx.author.roles, id=646549329493884929) or discord.utils.get(ctx.author.roles, id=646549322682466305) or discord.utils.get(ctx.author.roles, id=646551227626160139) or discord.utils.get(ctx.author.roles, id=673008336010084378) or discord.utils.get(ctx.author.roles, id=646549330479546379):
                    if cog.qualified_name == "Council Cog":
                        continue
                if cog.qualified_name == "Commands Cog":
                    continue
                embed.add_field(name=cog.qualified_name, value="`" + "`, `".join([c.name for c in cog.get_commands()]) + "`", inline=False)
            embed.set_footer(text=f"Use !beta-help <command> for more info on a command| Redwood Automation | Developed by {self.bot.owner}", icon_url=str(self.bot.user.avatar))
            await ctx.send(embed=embed)
        else:
            if (cmd := self.bot.get_command(command)) is not None:
                embed = discord.Embed(title=f"Help for {cmd.name}", description=cmd.help, color=0x00ff00)
                embed.add_field(name="Usage", value=f"`{cmd.signature}`", inline=False)
                if cmd.aliases:
                    embed.add_field(name="Aliases", value="`" + "`, `".join(cmd.aliases) + "`" or None, inline=False)
                if isinstance(cmd, commands.Command):
                    embed.add_field(name="Cooldown", value=cmd._buckets._cooldown.per or None, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("That command doesn't exist.")
                pass
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(HelpCog(bot))