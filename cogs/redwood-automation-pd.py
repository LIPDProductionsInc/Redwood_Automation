import discord
import datetime
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

#Descriptions

open_description = """Are you ready to make a difference? The Redwood Police Department is excited to announce that we are now accepting applications for dedicated individuals who are passionate about upholding the values of safety, integrity, and community.

Join our ranks and become a part of a team that values diversity, teamwork, and continuous growth. As a Redwood police officer, you'll receive comprehensive training, access to cutting-edge resources, and the chance to build lasting connections within our community."""

class RedwoodAutomationPD(commands.Cog, name="Police Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(name="applications", description="Opens and closes applications for the Redwood Police Department.")
    @commands.has_role(1005949022248378469)
    @app_commands.describe(status="Open or Close applications")
    async def applications(self, ctx: commands.Context, status: Literal["Open", "Transfer Only" "Close", "Init"]) -> None:
        if ctx.guild.id == 1005182438265335901:
            channel = ctx.bot.get_channel(1026530495569346590)
            city_channel = ctx.bot.get_channel(646541531523710996)
            if status == "Open":
                embed = discord.Embed(
                    title="Redwood Police Department Applications are OPEN!",
                    colour=discord.Color(0x007713),
                    type="rich",
                    description=open_description
                )
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
                embed.set_footer(text="As a reminder, a valid POST certification is required")
                await channel.send(embed=embed)
                message = await city_channel.send(embed=embed)
                await message.publish()
                await ctx.send("Opened applications. Remember to delete any embeds in <#1026530495569346590> that say otherwise.", ephemeral=True)

    pass

async def setup(bot) -> None:
    await bot.add_cog(RedwoodAutomationPD(bot))
