import discord
import datetime
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

#Descriptions

class RedwoodAutomationPD(commands.Cog, name="Police Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(name="applications", description="Opens and closes applications for the Redwood Police Department.")
    @commands.has_role(1005949022248378469)
    @app_commands.describe(status="Open or Close applications")
    async def applications(self, ctx: commands.Context, status: Literal["Open", "Transfer Only" "Close", "Init"]) -> None:
        if ctx.guild.id == 1005182438265335901:

    pass

async def setup(bot) -> None:
    await bot.add_cog(RedwoodAutomationPD(bot))
