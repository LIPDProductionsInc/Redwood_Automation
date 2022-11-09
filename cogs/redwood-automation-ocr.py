import discord

from discord.ext import commands

class RedwoodAutomationOCR(commands.Cog, name="Office of Commerce Relations Commands"):
    def __init__(self, bot) -> None:
       self.bot = bot

   #Commands go here

async def setup(bot: commands.Bot) -> None:
    bot.add_cog(RedwoodAutomationOCR(bot))