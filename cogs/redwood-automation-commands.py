import discord

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class CommandsCog(commands.Cog, name="Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.guild_only()
    async def ping_command(self, ctx: commands.Context):
        embed=discord.Embed(
            colour=discord.Color.green(),
            description=f''':ping_pong: ***Pong!***
**Latency:** {round(self.bot.latency * 1000)}ms'''
            )
        await ctx.send(embed=embed)
        pass

    @commands.hybrid_command(name="source", description="Get the source code of the bot.")
    @commands.guild_only()
    async def source_command(self, ctx: commands.Context):
        await ctx.send("Check out the source code for Redwood Deli and help add to the bot here: https://github.com/LIPDProductionsInc/Redwood_Automation")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))