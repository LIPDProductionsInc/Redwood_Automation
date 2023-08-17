import discord
import datetime

from discord.ext import commands

class RedwoodAutomationPD(commands.Cog, name="Police Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    #Commands

    pass

async def setup(bot) -> None:
    await bot.add_cog(RedwoodAutomationPD(bot))