import discord
import datetime

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
        embed.add_field(name="Council Chairperson", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=673008336010084378)}, inline=False)
        embed.add_field(name="Council Members", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549329493884929)]), inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=self.bot.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))