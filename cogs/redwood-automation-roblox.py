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

    group = app_commands.Group(name='get', description="Get commands")

    @commands.command(name='roblox-connect', hidden=True)
    @commands.is_owner()
    async def _test(self, ctx):
        user = await client.get_authenticated_user()
        await ctx.send(f'Logged in as `{user.name}`:`{user.id}`')
        pass

    @group.command(name='departments', description="Get the departments the user is in")
    async def departments_command(self, interaction: discord.Interaction, roblox_id: int):
        user = await client.get_user(roblox_id)
        roles = await user.get_group_roles()
        role = None
        for final_role in roles:
            if final_role.group.id == 14725251: #RPD
                role = final_role
                break
        print(role)
        #Departments
        #apd = client.get_base_group(14089278)
        #pdp = client.get_base_group(4431799)
        #scpa = client.get_base_group(11324038)
        #scfd = client.get_base_group(2805393)
        #scso = client.get_base_group(2805388)
        #fps = client.get_base_group(5684663)
        #fbi = client.get_base_group(3411434)
        #doa = client.get_base_group(2890690)
        #dos = client.get_base_group(2842177)
        #doh = client.get_base_group(2826521)
        #courts = client.get_base_group(2825030)
        #dpw = client.get_base_group(2811838)
        #dps = client.get_base_group(2809133)
        #docm = client.get_base_group(2808791)
        #doc = client.get_base_group(2807789)
        #doj = client.get_base_group(2803369)
        #dot = client.get_base_group(2803367)
        #fng = client.get_base_group(2803372)
        #fsp = client.get_base_group(2803364)
        #Checks
        await interaction.response.send_message('Test sent', ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxCommandsCog(bot))