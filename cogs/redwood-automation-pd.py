import discord
import datetime
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

#Descriptions

open_description = """Are you ready to make a difference? The Redwood Police Department is excited to announce that we are now accepting applications for dedicated individuals who are passionate about upholding the values of safety, integrity, and community.

Join our ranks and become a part of a team that values diversity, teamwork, and continuous growth. As a Redwood police officer, you'll receive comprehensive training, access to cutting-edge resources, and the chance to build lasting connections within our community."""

transfer_description = "Attention law enforcement professionals! Exciting news: transfer applications are now open for those seeking to bring their skills and dedication to the Redwood Police Department. Take the next step in your career journey and become an integral part of our dynamic team. Apply today and be a force for positive change in our community. Your experience matters - let's make a difference together at RPD!"

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
            elif status == "Transfer Only":
                embed = discord.Embed(
                    title="Redwood Police Department General Applications",
                    colour=discord.Color(0xbb7000),
                    type="rich",
                    description="The Redwood Police Department do not currently have applications open to the general public."
                )
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1047644039870152794/1137541647534661762/Screenshot_99.png")
                embed2 = discord.Embed(
                    title="Redwood Police Department Transfer Applications",
                    colour=discord.Color(0x007713),
                    type="rich",
                    description=transfer_description
                )
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
                embed2.set_image(url="https://cdn.discordapp.com/attachments/975458359501271070/1135769455364935771/Screenshot_66.png")
                await channel.send(embed=embed)
                await channel.send(embed=embed2)
                message = await city_channel.send(embed=embed2)
                await message.publish()
                await ctx.send("Transfer Applications opened. Remember to delete any embeds in <#1026530495569346590> that say otherwise.", ephemeral=True)

    pass

async def setup(bot) -> None:
    await bot.add_cog(RedwoodAutomationPD(bot))
