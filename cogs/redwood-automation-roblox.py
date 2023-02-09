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
    @app_commands.describe(roblox_id="The Roblox ID of the user")
    async def departments_command(self, interaction: discord.Interaction, roblox_id: int):
        user = await client.get_user(roblox_id)
        roles = await user.get_group_roles()
        #Departments
        for final_role in roles:
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
            if final_role.group.id == 14725251: #RPD
                rpd = final_role.name
            if final_role.group.id == 14089278: #APD
                apd = final_role.name
            if final_role.group.id == 4431799: #PDP
                pdp = final_role.name
            if final_role.group.id == 11324038: #SCPA
                scpa = final_role.name
            if final_role.group.id == 2805393: #SCFD
                scfd = final_role.name
            if final_role.group.id == 2805388: #SCSO
                scso = final_role.name
            if final_role.group.id == 5684663: #FPS
                fps = final_role.name
            if final_role.group.id == 3411434: #FBI
                fbi = final_role.name
            if final_role.group.id == 2890690: #DOA
                doa = final_role.name
            if final_role.group.id == 2842177: #DOS
                dos = final_role.name
            if final_role.group.id == 2826521: #DOH
                doh = final_role.name
            if final_role.group.id == 2825030: #Courts
                courts = final_role.name
            if final_role.group.id == 2811838: #DPW
                dpw = final_role.name
            if final_role.group.id == 2809133: #DPS
                dps = final_role.name
            if final_role.group.id == 2808791: #DOCM
                docm = final_role.name
            if final_role.group.id == 2807789: #DOC
                doc = final_role.name
            if final_role.group.id == 2803369: #DOJ
                doj = final_role.name
            if final_role.group.id == 2803367: #DOT
                dot = final_role.name
            if final_role.group.id == 2803372: #FNG
                fng = final_role.name
            if final_role.group.id == 2803364: #FSP
                fsp = final_role.name
        embed = discord.Embed(
            title=f"{user.name}'s Departments",
            colour=discord.Colour.dark_blue()
        )
        if rpd != "Guest":
            embed.add_field(name="Redwood Police Department", value=rpd)
        if apd != "Guest":
            embed.add_field(name="Arborfield Police Department", value=apd)
        if pdp != "Guest":
            embed.add_field(name="Promience District Police", value=pdp)
        if scpa != "Guest":
            embed.add_field(name="Stapleton County Port Authroity", value=scpa)
        if scfd != "Guest":
            embed.add_field(name="Stapleton County Fire Department", value=scfd)
        if scso != "Guest":
            embed.add_field(name="Stapleton County Sheriff's Office", value=scso)
        if fps != "Guest":
            embed.add_field(name="Firestone Park Service", value=fps)
        if fbi != "Guest":
            embed.add_field(name="Firestone Bureau of Investigation", value=fbi)
        if doa != "Guest":
            embed.add_field(name="Department of Aviation", value=doa)
        if dos != "Guest":
            embed.add_field(name="Department of State", value=dos)
        if doh != "Guest":
            embed.add_field(name="Department of Health", value=doh)
        if courts != "Guest":
            embed.add_field(name="Firestone Courts", value=courts)
        if dpw != "Guest":
            embed.add_field(name="Department of Public Works", value=dpw)
        if dps != "Guest":
            embed.add_field(name="Department of Public Safety", value=dps)
        if docm != "Guest":
            embed.add_field(name="Department of Commerce", value=docm)
        if doc != "Guest":
            embed.add_field(name="Department of Corrections", value=doc)
        if doj != "Guest":
            embed.add_field(name="Department of Justice", value=doj)
        if dot != "Guest":
            embed.add_field(name="Department of Transportation", value=dot)
        if fng != "Guest":
            embed.add_field(name="Firestone National Guard", value=fng)
        if fsp != "Guest":
            embed.add_field(name="Firestone State Police", value=fsp)
        if len(embed.fields) == 0:
            embed.description = "This user is not in any departments"
        '''If a user is in two or more primary departments and not the Founder, make the description say that'''
        #List the Primary Departments Here
        '''If a user is in three or more secondary departments and not the Founder, make the description say that'''
        #List the Secondary Departments Here
        #embed.set_thumbnail(url=ROBLOX_AVATAR)
        embed.set_footer(text=f"Redwood Automation | Requested by: {interaction.user.name}")
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)
        pass

    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(RobloxCommandsCog(bot))