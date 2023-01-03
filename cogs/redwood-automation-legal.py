import discord
import datetime

from discord.ext import commands

class LegalOfficeCog(commands.Cog, name="City Attorney Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="legal-office", description="View the current members of the City Attorney's Office.")
    async def legal_office(self, ctx):
        embed = discord.Embed(
            title="Redwood City Attorney's Office",
            description="The current members of the City Attorney's Office are as follows:",
            colour=discord.Color.dark_blue()
        )
        embed.add_field(name="City Attorney", value=[member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549330479546379) and discord.utils.get(member.roles, id=763470466269577216)][0], inline=True)
        if len(discord.utils.get(ctx.guild.roles, id=646549330479546379).members) == 2:
            embed.add_field(name="Assistant City Attorney", value=[member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549330479546379) and not discord.utils.get(member.roles, id=763470466269577216)][0], inline=False)
        else:
            embed.add_field(name="Assistant City Attorneys", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549330479546379) and not discord.utils.get(member.roles, id=763470466269577216)]), inline=False)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot):
    await bot.add_cog(LegalOfficeCog(bot))