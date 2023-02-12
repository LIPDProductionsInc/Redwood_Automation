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
        user = await client.get_user(roblox_id)
        roles = await user.get_group_roles()
        #Departments
        rpd = "Guest"
        apd = "Guest"
        pdp = "Guest"
        scpa = "Guest"
        scfd = "Guest"
        scso = "Guest"
        fps = "Guest"
        fbi = "Guest"
        doa = "Guest"
        dos = "Guest"
        doh = "Guest"
        courts = "Guest"
        dpw = "Guest"
        dps = "Guest"
        docm = "Guest"
        doc = "Guest"
        doj = "Guest"
        dot = "Guest"
        fng = "Guest"
        fsp = "Guest"
        for role in roles:
            if role.group.id == 14725251: #RPD
                rpd = role.name
            if role.group.id == 14089278: #APD
                apd = role.name
            if role.group.id == 4431799: #PDP
                pdp = role.name
            if role.group.id == 11324038: #SCPA
                scpa = role.name
            if role.group.id == 2805393: #SCFD
                scfd = role.name
            if role.group.id == 2805388: #SCSO
                scso = role.name
            if role.group.id == 5684663: #FPS
                fps = role.name
            if role.group.id == 3411434: #FBI
                fbi = role.name
            if role.group.id == 2890690: #DOA
                doa = role.name
            if role.group.id == 2842177: #DOS
                dos = role.name
            if role.group.id == 2826521: #DOH
                doh = role.name
            if role.group.id == 2825030: #Courts
                courts = role.name
            if role.group.id == 2811838: #DPW
                dpw = role.name
            if role.group.id == 2809133: #DPS
                dps = role.name
            if role.group.id == 2808791: #DOCM
                docm = role.name
            if role.group.id == 2807789: #DOC
                doc = role.name
            if role.group.id == 2803369: #DOJ
                doj = role.name
            if role.group.id == 2803367: #DOT
                dot = role.name
            if role.group.id == 2803372: #FNG
                fng = role.name
            if role.group.id == 2803364: #FSP
                fsp = role.name
        embed = discord.Embed(
            title=f"{user.name}'s Departments",
            colour=discord.Colour.dark_blue()
        )
        if rpd not in ["Guest"]:
            embed.add_field(name="Redwood Police Department", value=rpd, inline=False)
        if apd not in ["Guest"]:
            embed.add_field(name="Arborfield Police Department", value=apd, inline=False)
        if pdp not in ["Guest"]:
            embed.add_field(name="Promience District Police", value=pdp, inline=False)
        if scpa not in ["Guest"]:
            embed.add_field(name="Stapleton County Port Authroity", value=scpa, inline=False)
        if scfd not in ["Guest"]:
            embed.add_field(name="Stapleton County Fire Department", value=scfd, inline=False)
        if scso not in ["Guest"]:
            embed.add_field(name="Stapleton County Sheriff's Office", value=scso, inline=False)
        if fps not in ["Guest"]:
            embed.add_field(name="Firestone Park Service", value=fps, inline=False)
        if fbi not in ["Guest"]:
            embed.add_field(name="Firestone Bureau of Investigation", value=fbi, inline=False)
        if doa not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Department of Aviation", value=doa, inline=False)
        if dos not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Department of State", value=dos, inline=False)
        if doh not in ["Guest"]:
            embed.add_field(name="Department of Health", value=doh, inline=False)
        if courts not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Firestone Courts", value=courts, inline=False)
        if dpw not in ["Guest"]:
            embed.add_field(name="Department of Public Works", value=dpw, inline=False)
        if dps not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Department of Public Safety", value=dps, inline=False)
        if docm not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Department of Commerce", value=docm, inline=False)
        if doc not in ["Guest"]:
            embed.add_field(name="Department of Corrections", value=doc, inline=False)
        if doj not in ["Guest", "Firestone Citizen"]:
            embed.add_field(name="Department of Justice", value=doj, inline=False)
        if dot not in ["Guest"]:
            embed.add_field(name="Department of Transportation", value=dot, inline=False)
        if fng not in ["Guest"]:
            embed.add_field(name="Firestone National Guard", value=fng, inline=False)
        if fsp not in ["Guest"]:
            embed.add_field(name="Firestone State Police", value=fsp, inline=False)
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
