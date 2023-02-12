import discord
import datetime
import typing

from discord import app_commands
from discord.ext import commands
from typing import Literal

class EASCog(commands.Cog, name="Emergency Alert System"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name="eas-init", hidden=True)
    @commands.check_any(commands.is_owner(), commands.has_role(1038941326047191161))
    async def eas_init(self, ctx: commands.Context) -> None:
        channel = ctx.bot.get_channel(1050019636231536690)
        embed = discord.Embed(
            title="Redwood City Emergency Alert System",
            colour=discord.Color.dark_blue(),
            description="This is the Redwood City Emergency Alert System. This system is used to alert Redwood City residents of any emergencies or incidents that may occur. This system is only used in the event of an emergency or an important incident."
        )
        embed.add_field(name="Levels of Emergency", value=":green_square: | (Level 1) | Normal Operations\n:white_large_square: | (Level 2) | City Holiday (Reduced Operations)\n:yellow_square: | (Level 3) | Notices and Weather Advisories\n:orange_square: | (Level 4) | Weather Watches, Warnings, and Minor Emergencies\n:red_square: | (Level 5) | Major Weather Event and City Emergencies", inline=False)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text="The Redwood City Emergency Alert System is maintained by the Redwood Executive Emergency Committee. They are responsible for issuing alerts as needed.")
        await channel.send(embed=embed)
        pass

    @commands.hybrid_command(name="issue", description="Issues an alert or return to normal operations")
    @commands.check_any(commands.is_owner(), commands.has_role(1038941326047191161))
    @app_commands.describe(level="The level of the alert to issue", message="The message to send with the alert (If not normal/holiday)")
    async def issue(self, ctx: commands.Context, level: Literal["Normal Operations", "City Holiday", "City Notice", "Weather Watch", "Weather Warning", "Minor Emergency", "Major Weather Event (State of Emergency)", "State of Emergency"], *, message: str = None) -> None:
        channel = ctx.bot.get_channel(1050019636231536690)
        if level == "Normal Operations":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.green()
            )
            embed.add_field(name=":green_square: | Normal Operations", value="The City of Redwood City is currently operating under normal conditions. There are no emergencies or incidents that are currently affecting the city.", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text="Issued:")
            embed.timestamp = datetime.datetime.now()
        elif level == "City Holiday":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.light_grey()
            )
            embed.add_field(name=":white_large_square: | City Holiday", value="The City of Redwood City is currently on a city holiday. Non-essential city services are closed for the day. Essential services will remain open.", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "City Notice":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.gold()
            )
            embed.add_field(name=":yellow_square: | City Notice", value=message, inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "Weather Advisory":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.gold()
            )
            embed.add_field(name=":yellow_square: | Weather Advisory", value=f"The Stapleton County Weather Service has issued a Weather Advisory for the City of Redwood. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "Weather Watch":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.orange()
            )
            embed.add_field(name=":orange_square: | Weather Watch", value=f"The Stapleton County Weather Service has issued a Weather Watch for the City of Redwood. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "Weather Warning":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.orange()
            )
            embed.add_field(name=":orange_square: | Weather Warning", value=f"The Stapleton County Weather Service has issued a Weather Warning for the City of Redwood. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "Minor Emergency":
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.orange()
            )
            embed.add_field(name=":orange_square: | Minor Emergency", value=f"There is currently an emergency event in progress in the City of Redwood. A City Emergency has **not** been declared at this time. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
        elif level == "Major Weather Event (City Emergency)":
            channel2 = ctx.bot.get_channel(646541531523710996)
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.red()
            )
            embed.add_field(name=":red_square: | Major Weather Event (City Emergency Issued)", value=f"There is currently a major weather event in progress in the City of Redwood. A City Emergency has been declared. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
            await channel2.send("@everyone", embed=embed)
        elif level == "State of Emergency":
            channel2 = ctx.bot.get_channel(646541531523710996)
            embed = discord.Embed(
                title="Redwood City Emergency Alert System",
                colour=discord.Color.red()
            )
            embed.add_field(name=":red_square: | City Emergency", value=f"A City Emergency has been declared for the City of Redwood. Details can be found below:\n\n{message}", inline=False)
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            embed.set_footer(text=f"Issued by {ctx.author.display_name} at:")
            embed.timestamp = datetime.datetime.now()
            await channel2.send("@everyone", embed=embed)
        await channel.send(embed=embed)
        await ctx.send("Issued!", ephemeral=True)
        pass

    @commands.hybrid_command(name="emergency-committee", description="View the current members of the Emergency Committee.", alaises=["reec"])
    @commands.guild_only()
    async def emergency_committee(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Redwood City Executive Emergency Committee",
            description="The current members of the Redwood Executive Emergency Committee are as follows:",
            colour=discord.Color.dark_blue()
        )
        embed.add_field(name="Mayor", value=ctx.guild.get_role(646549322682466305).members[0].mention if len(ctx.guild.get_role(646549322682466305).members) > 0 else "VACANT", inline=True)
        embed.add_field(name="Deputy Mayor", value=ctx.guild.get_role(646551227626160139).members[0].mention if len(ctx.guild.get_role(646551227626160139).members) > 0 else "VACANT", inline=True)
        embed.add_field(name="Committee Advisor", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=1038941326047191161) and not discord.utils.get(member.roles, id=646549322682466305) and not discord.utils.get(member.roles, id=646551227626160139)]), inline=False)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EASCog(bot))