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
            fs_group_ids = [14725251, 14089278, 4431799, 11324038, 2805393, 2805388, 5684663, 3411434, 2890690, 2842177, 2826521, 2825030, 2811838, 2809133, 2808791, 2807789, 2803369, 2803367, 2803372, 2803364, 15301612]
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
            embed.add_field(name=user_role.group.name, value=user_role.name, inline=False)
        if len(embed.fields) == 0:
            embed.description = "This user is not in any departments"
        #Primary and Secondary Departments Check
        primary_departments = ["Firestone Bureau of Investigation", "Firestone State Patrol", "Firestone Park Service", "Stapleton County Sheriff's Office", "Redwood Police Department", "Arborfield Police Department", "Promience District Police"]
        secondary_departments = ["Firestone Department of Corrections", "Firestone Department of Public Safety", "Firestone Department of Public Works", "Firestone Department of Transportation", "Firestone Department of Health", "Firestone Aviation Administration", "Firestone Department of Aviation", "Stapleton County Port Authority"]
        primaries = 0
        secondaries = 0
        for field in embed.fields:
            if field.name in primary_departments:
                primaries += 1
                #SCFD Special Check
                if field.name == "Stapleton County Fire Department":
                    if user_role.rank >= 40:
                        primaries += 1
                    else:
                        secondaries += 1
            if field.name in secondary_departments:
                secondaries += 1
        if primaries >= 2 and user_role.name != "Founder" or user_role.name != "Firestone Developer":
            primary_check = True
        else:
            primary_check = False
        if secondaries >= 3 and user_role.name != "Founder" or user_role.name != "Firestone Developer":
            secondary_check = True
        else:
            secondary_check = False
        if primary_check == True:
            if embed.description == None:
                embed.description = f"**WARNING:** This user has **{primaries} primary departments.** This is not allowed."
            else:
                embed.description += f"\n**WARNING:** This user has **{primaries} primary departments.** This is also not allowed."
                pass
            pass
        if secondary_check == True:
            if embed.description == None:
                embed.description = f"**WARNING:** This user has **{secondaries} secondary departments.** This is not allowed."
            else:
                embed.description += f"\n**WARNING:** This user has **{secondaries} secondary departments.** This is also not allowed."
                pass
            pass
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
