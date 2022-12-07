import discord
import datetime

from discord import app_commands
from discord.ext import commands

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    #Commands for the Mayor's Office

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))