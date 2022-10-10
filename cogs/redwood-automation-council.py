from random import choices
from typing import Literal
import discord
import datetime

from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class CouncilCog(commands.Cog, name="Council Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="council", description="Shows the current city council members.")
    @commands.guild_only()
    async def council(self, ctx):
        embed = discord.Embed(
            title="Redwood City Council",
            description="Here is a list of the current city council members.",
            color=discord.Color.dark_blue()
            )
        embed.add_field(name="Mayor", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549322682466305)}, inline=True)
        embed.add_field(name="Deputy Mayor", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646551227626160139)}, inline=True)
        embed.add_field(name="City Council Chairperson", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=673008336010084378)}, inline=False)
        embed.add_field(name="City Council Members", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549329493884929)]), inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=self.bot.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="docket", description="Has the bot announce the next item on the city council docket.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    
    async def docket(self, ctx, first: Literal[True, False], docket_item, docket_link):
        """If the item is the first item of the session, the bot will announce as such. Otherwise, it will announce the next item on the docket."""
        #if ctx.category_id == 646552329654370345:
        if first == True:
            await ctx.send(f"The first item on the docket is {docket_item}. \n\n{docket_link} \n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
        else:
            await ctx.send(f"The next item on the docket is {docket_item}. \n\n{docket_link} \n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))