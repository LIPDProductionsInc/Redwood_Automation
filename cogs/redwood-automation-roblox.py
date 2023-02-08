import discord
import datetime
import os
import roblox

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from roblox import Client
from roblox.bases.basegroup import BaseGroup

load_dotenv()
client = Client(os.getenv("RobloxToken"))

class RobloxCommandsCog(commands.Cog, name="ROBLOX Related Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='roblox-connect', hidden=True)
    @commands.is_owner()
    async def _test(self, ctx):
        user = await client.get_authenticated_user()
        await ctx.send(f'Logged in as {user.name}:{user.id}')
        pass

    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxCommandsCog(bot))