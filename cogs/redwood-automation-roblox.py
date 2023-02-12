import discord
import datetime
import os
import roblox

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from roblox import Client
from roblox.bases.basegroup import BaseGroup
from roblox.thumbnails import AvatarThumbnailType

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
    @app_commands.describe(roblox_id="The Roblox ID of the user")
    async def departments_command(self, interaction: discord.Interaction, roblox_id: int):
        def group_check(user_role):
            fs_group_ids = [14725251, 14089278, 4431799, 11324038, 2805393, 2805388, 5684663, 3411434, 2890690, 2842177, 2826521, 2825030, 2811838, 2809133, 2808791, 2807789, 2803369, 2803367, 2803372, 2803364]
            blocked_roles = ["Guest", "Firestone Citizen"]
            if user_role.group.id in fs_group_ids and user_role.name not in blocked_roles:
              return True
            else:
              return False
        
        user = await client.get_user(roblox_id)
        groups = await user.get_group_roles()
        
        filtered_groups = filter(group_check, groups)
        embed = discord.Embed(
            title=f"{user.name}'s Departments",
            colour=discord.Colour.dark_blue()
        )
        for user_role in list(filtered_groups):
            embed.add_field(name=user_role.group.name, value=user_role.role_name, inline=False)
        if len(embed.fields) == 0:
            embed.description = "This user is not in any departments"
        '''If a user is in two or more primary departments and not the Founder, make the description say that'''
        #List the Primary Departments Here
        '''If a user is in three or more secondary departments and not the Founder, make the description say that'''
        #List the Secondary Departments Here
        avatar = await client.thumbnails.get_user_avatar_thumbnails([roblox_id], type=AvatarThumbnailType.headshot, size=(150, 150))
        embed.set_thumbnail(url=avatar[0].image_url)
        embed.set_footer(text=f"Redwood Automation | Requested by: {interaction.user.name}")
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)
        pass

    @group.command(name="certifications", description="Shows a user's certifications")
    @app_commands.describe(roblox_id="The user's Roblox ID")
    async def certifications(self, interaction: discord.Interaction, roblox_id: int):
        user = await client.get_user(roblox_id)
        roles = await user.get_group_roles()
        ffa = "None Obtainable"
        post = "None Obtainable"
        for role in roles:
            if role.group.id == 2979146: #FFA
                ffa = role.name
            if role.group.id == 2808300: #POST
                post = role.name
        embed = discord.Embed(
            title=f"{user.name}'s Certifications",
            colour=discord.Colour.dark_blue()
        )
        embed.add_field(name="Firestone Fire Academy", value=ffa, inline=False)
        embed.add_field(name="Peace Officer Standards and Training", value=post, inline=False)
        if len(embed.fields) == 0 or len(embed.fields) == 1:
            raise TypeError(f"Expected 2 fields, got {len(embed.fields)}")
        avatar = await client.thumbnails.get_user_avatar_thumbnails([roblox_id], type=AvatarThumbnailType.headshot, size=(150, 150))
        embed.set_thumbnail(url=avatar[0].image_url)
        embed.set_footer(text=f"Redwood Automation | Requested by: {interaction.user.name}")
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)
        pass

    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxCommandsCog(bot))
