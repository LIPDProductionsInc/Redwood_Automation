import discord
import datetime

from discord.ext import commands
from datetime import timedelta

class HelpCog(commands.Cog, name="Help Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx:commands.Context, *, command:str = None) -> None:
        """Shows help about a command or the bot"""
        if command is None:
            embed = discord.Embed(
                title="Help",
                description="Here is a list of commands you can use with Redwood Automation.",
                color=discord.Color.dark_blue()
                )
            if discord.utils.get(ctx.author.roles, id=1150770058914705533):
                embed.add_field(name="Council Commands", value="`propose`, `legal-review`, `charter`, `template`, `documents`", inline=False)
            if discord.utils.get(ctx.author.roles, id=1150770058914705534) or discord.utils.get(ctx.author.roles, id=1150770058935681160) or discord.utils.get(ctx.author.roles, id=1150770058935681162):
                embed.add_field(name="Presiding Officer Commands", value="`docket`, `session`, `end-session`, `floor`, `dismiss`, `send`, `documents`, `elections`", inline=False)
            if discord.utils.get(ctx.author.roles, id=1150770058914705528):
                embed.add_field(name="City Attorney Commands", value="`send`, `documents`", inline=False)
            if discord.utils.get(ctx.author.roles, id=1150770058897920156):
                embed.add_field(name="Emergency Executive Committee Commands", value="`eas-init`, `issue`", inline=False)
                embed.add_field(name="Mayor Commands", value="`appoint`, `seal`", inline=False)
                embed.add_field(name="Deputy Mayor Commands", value="`appoint`, `seal`", inline=False)
            if discord.utils.get(ctx.author.roles, id=1150770058935681162):
            if discord.utils.get(ctx.author.roles, id=1150770058935681160):
            if discord.utils.get(ctx.author.roles, id=1150770058897920159):
                embed.add_field(name="Press Office Commands", value="`seal`, `tweet`", inline=False)
            if discord.utils.get(ctx.author.roles, id=1150770058897920157):
                embed.add_field(name="City Clerk Commands", value="`transcript`, `bulletin`", inline=False)
            embed.add_field(name="Commands", value="`help`, `ping`, `serverinfo`, `userinfo`, `avatar`, `council`, `legal-office`, `complaint`, `feedback`, `polls`", inline=False)
            if ctx.author.guild_permissions.moderate_members:
                embed.add_field(name="Moderation", value="`ban`, `kick`, `unban`", inline=False)
            embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner}", icon_url=str(self.bot.user.avatar))
            await ctx.send(embed=embed)
        else:
            if (cmd := self.bot.get_command(command)) is not None:
                #Insert stuff here to make sure the command is allowed to be used by the user. Return True or False.
                perms = "Not Set"
                if perms:
                    embed = discord.Embed(
                        title=f"Help for {cmd.name}",
                        description=cmd.describe,
                        color=discord.Color.dark_blue()
                        )
                    embed.add_field(name="Usage", value=f"`{cmd.signature}`", inline=False)
                    if cmd.aliases:
                        embed.add_field(name="Aliases", value="`" + "`, `".join(cmd.aliases) + "`", inline=False)
                    if cmd._buckets._cooldown:
                        embed.add_field(name="Cooldown", value=f"{cmd._buckets._cooldown.per} seconds", inline=False)
                    await ctx.send(embed=embed)
                elif perms == False:
                    await ctx.send("You do not have permission to use this command.", ephemeral=True)
                else:
                    raise AttributeError(f"Expected a boolean value for perms, got {perms} instead.")
            else:
                await ctx.send("That command does not exist.", ephemeral=True)
        pass

    @commands.command(name="beta-help", description="Shows help about a command or the bot (Beta version)", aliases=["help-beta"], hidden=True)
    @commands.is_owner()
    async def help_beta(self, ctx:commands.Context, *, command:str = None) -> None:
        if command is None:
            embed = discord.Embed(title="Help", description="Here's a list of all my commands:", colour=discord.Colour.dark_blue())
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
                embed = discord.Embed(title=f"Help for {cmd.name}", description=cmd.describe, colour=discord.Colour.dark_blue())
                embed.add_field(name="Usage", value=f"`{cmd.signature}`", inline=False)
                if cmd.aliases:
                    embed.add_field(name="Aliases", value="`" + "`, `".join(cmd.aliases) + "`", inline=False)
                if cmd._buckets._cooldown:
                    embed.add_field(name="Cooldown", value=f"{cmd._buckets._cooldown.per} seconds", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("That command doesn't exist.")
                pass
            pass
        pass

    pass

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
