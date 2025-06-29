import discord
import datetime
import typing

from discord.ext import commands, menus
from discord import app_commands
from datetime import timedelta
from typing import Literal

class MDTEmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        embed.type = 'rich'
        embed.set_author(name="Redwood Police Department Mobile Data Terminal", icon_url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
        embed.colour = discord.Color.blue()
        embed.timestamp=datetime.datetime.now()
        owner = discord.utils.get(menu.ctx.guild.members, id=menu.ctx.bot.owner_id)
        return embed.set_footer(text=f"To suggest items to be added, please contact NCISfan5 | Developed by {owner} | Accurate as of:")
    pass

#Descriptions

open_description = """Are you ready to make a difference? The Redwood Police Department is excited to announce that we are now accepting applications for dedicated individuals who are passionate about upholding the values of safety, integrity, and community.

Join our ranks and become a part of a team that values diversity, teamwork, and continuous growth. As a Redwood police officer, you'll receive comprehensive training, access to cutting-edge resources, and the chance to build lasting connections within our community."""

transfer_description = "Attention law enforcement professionals! Exciting news: transfer applications are now open for those seeking to bring their skills and dedication to the Redwood Police Department. Take the next step in your career journey and become an integral part of our dynamic team. Apply today and be a force for positive change in our community. Your experience matters - let's make a difference together at RPD!"

init_description = """Greetings, citizens and visitors alike. We are honored to extend a warm welcome to you within the confines of our law enforcement community. The Redwood Police Department is committed to serving and safeguarding our vibrant city with utmost dedication and professionalism.

As the guardians of peace, safety, and justice, our officers and staff uphold the values of integrity, compassion, and excellence in every facet of their duties. With a shared mission to protect and support, we stand vigilant against adversity and are dedicated to fostering a secure environment where all can thrive.

Whether you're here seeking assistance, reporting a concern, or simply engaging with our community outreach initiatives, know that your presence matters to us. We embrace collaboration, communication, and community involvement as cornerstones of our approach to policing.

Join us in creating a harmonious and secure Redwood where every individual can enjoy the benefits of living in a place where safety and unity prevail. Together, we shape the future, one step at a time.

Once again, welcome to the Redwood Police Department. We stand ready to serve, protect, and make a positive impact, side by side with you."""

class RedwoodAutomationPD(commands.Cog, name="Police Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="applications", description="Opens and closes applications for the Redwood Police Department.")
    @app_commands.checks.has_role(1005949022248378469) # RPD Chief of Police
    @app_commands.guilds(1005182438265335901) # Redwood Police Department server
    @app_commands.describe(status="Open or Close applications")
    async def applications(self, interaction: discord.Interaction, status: Literal["Open", "Transfer Only" "Close", "Init"]) -> None:
        channel = self.bot.get_channel(1026530495569346590)
        city_channel = self.bot.get_channel(1151380671126839386)
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
            await interaction.response.send_message("Opened applications. Remember to delete any embeds in <#1026530495569346590> that say otherwise.", ephemeral=True)
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
            await interaction.response.send_message("Transfer Applications opened. Remember to delete any embeds in <#1026530495569346590> that say otherwise.", ephemeral=True)
        elif status == "Close":
            embed = discord.Embed(
                title="Redwood Police Department General Applications",
                colour=discord.Color(0x920707),
                type="rich",
                description="The Redwood Police Department regrets to inform you that our application process is currently closed. Please keep an eye on this channel for updates on when we have opened them up once again."
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1047644039870152794/1140329049303040050/Screenshot_143.png")
            await channel.send(embed=embed)
            message = await city_channel.send(embed=embed)
            await message.publish()
            await interaction.response.send_message("Closed applications. Remember to delete any embeds in <#1026530495569346590> that say otherwise.", ephemeral=True)
        elif status == "Init":
            embed = discord.Embed(
                title="The Redwood Police Department",
                colour=discord.Color(0x004272),
                type="rich",
                description=init_description
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041839113000726558/1142198375291289640/RPD_Seal.png")
            embed.set_image(url="https://cdn.discordapp.com/attachments/561690984803598346/1135257342158585978/image.png")
            await channel.send(embed=embed)
            await interaction.response.send_message("Initialized.")
        else:
            raise commands.BadArgument("Invalid status.")
        pass

    @commands.hybrid_command(name="mdt", description="Get the MDT")
    @commands.guild_only()
    async def mdt(self, ctx: commands.Context) -> None:
        message = await ctx.send("**Loading Mobile Data Terminal...**")
        embeds = [
            discord.Embed(
                title="Trello Boards",
                type="rich",
                description="**[Criminal Code](https://trello.com/b/EGN3OQzQ)**\n**[Traffic Violations Guide](https://trello.com/b/z1e04kAy)**\n**[District Court (For Warrants)](https://trello.com/b/KHYhrBju)**"
            ),
            discord.Embed(
                title="V2 Callout Map",
                type="rich"
            ).set_image(url="https://cdn.discordapp.com/attachments/362265369676873728/393423933249945600/unknown.png"),
            discord.Embed(
                title="V2 Road Name Map",
                type="rich"
            ).set_image(url="https://media.discordapp.net/attachments/323521773222232065/919633288627355698/FS_MAP.png"),
            discord.Embed(
                title="V2 Sewer Map",
                type="rich"
            ).set_image(url="https://media.discordapp.net/attachments/628034271570821120/1359054305319190649/image.png"),
            discord.Embed(
                title="RPD Trespass Zones (1st Floor)",
                description="Green = Public, Red = Restricted",
                type="rich"
            ).set_image(url="https://i.imgur.com/Taek1Sz.png"),
            discord.Embed(
                title="RPD Trespass Zones (2nd Floor)",
                description="Green = Public, Red = Restricted",
                type="rich"
            ).set_image(url="https://i.imgur.com/Jgee9lc.png"),
            discord.Embed(
                title="RPD Trespass Zones (Parking Lot)",
                description="Green = Public, Red = Restricted",
                type="rich"
            ).set_image(url="https://i.imgur.com/uIg4UN8.png"),
            discord.Embed(
                title="Databases",
                type="rich",
                description="**[FDOT Handicap Database](https://trello.com/b/vR54Te0o)**\n**[Firestone Firearms Commission](https://trello.com/b/YbN4xaAr)**\n**[FDOCM Business Permit Database](https://trello.com/b/r4a8Tw1I)**\n**[FAA Licenses](https://trello.com/b/1yOqOBhL)**\n**[Land Management](https://trello.com/b/v2fxXXhn)**\n**[POST Certifications](https://docs.google.com/spreadsheets/d/1vsa5klFFKEmezEJGeNYrVF3aGmMvUqH-U9mvZ1-LmV4/edit#gid=0)**"
            )
        ]
        menu = menus.MenuPages(source=MDTEmbedPageSource(embeds, per_page=1))
        await menu.start(ctx)
        await message.edit(content=f"**Loading Complete {ctx.author.mention}, don't catch a court case**")
        pass

    pass

async def setup(bot) -> None:
    await bot.add_cog(RedwoodAutomationPD(bot))
