import discord
import datetime
import sys
import traceback

from discord.ext import commands
from discord import app_commands

class ComplaintModal(discord.ui.Modal, title="Complaint Form", label="Test"):
    offender = discord.ui.TextInput(
        label="Who is your complaint against?",
        style=discord.TextStyle.short,
        placeholder="Enter their ROBLOX username and ID here...",
        required=True,
        min_length=3,
        max_length=100
    )

    department = discord.ui.TextInput(
        label="What department/office is the person in?",
        style=discord.TextStyle.short,
        placeholder="Enter the department/office here...",
        required=True,
        min_length=3,
        max_length=60
    )

    date = discord.ui.TextInput(
        label="What date did the incident occur?",
        style=discord.TextStyle.short,
        placeholder="Enter the date here...",
        required=True,
        min_length=6,
        max_length=100
    )

    complaint = discord.ui.TextInput(
        label="What is your complaint?",
        style=discord.TextStyle.long,
        placeholder="Enter your complaint here...",
        required=True,
        min_length=10,
        max_length=1000
    )

    additional = discord.ui.TextInput(
        label="List any evidence and/or witnesses here",
        style=discord.TextStyle.long,
        placeholder="Enter any evidence and/or witnesses here...",
        required=True,
        min_length=0
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you for your complaint! It has been sent for review. It can be seen by the Mayor, Deputy Mayor, RW Chief of Staff, City Attorneys Office, District Attorney, County Executive, and the Founder.", ephemeral=True)
        channel = interaction.client.get_channel(1034315223856840735)
        embed = discord.Embed(
            title="New Complaint",
            description=f"**Offender:**\n{self.offender.value}\n\n**Department/Office:**\n{self.department.value}\n\n**Date:**\n{self.date.value}\n\n**Complaint:**\n{self.complaint.value}\n\n**Evidence/Witnesses:**\n{self.additional.value}\n\n**Submitter:**\n{interaction.user.mention}",
            colour=discord.Color.dark_blue()
        )
        embed.set_footer(text=f"ID: {interaction.user.id}")
        embed.set_thumbnail(url=interaction.guild.me.avatar)
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("An error occurred while processing your complaint. Please try again later.", ephemeral=True)
        print('Ignoring exception in modal FeedbackModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        pass

    pass

class LegalOfficeCog(commands.Cog, name="City Attorney Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="legal-office", description="View the current members of the City Attorney's Office.")
    async def legal_office(self, ctx):
        city_attorney = 646549330479546379
        admin = 719393017848528928
        moderator = 646554162405834762
        embed = discord.Embed(
            title="Redwood City Attorney's Office",
            description="The current members of the City Attorney's Office are as follows:",
            colour=discord.Color.dark_blue()
        )
        embed.add_field(name="City Attorney", value=[member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=city_attorney) and discord.utils.get(member.roles, id=admin)][0], inline=True)
        if len(discord.utils.get(ctx.guild.roles, id=city_attorney).members) == 2:
            embed.add_field(name="Assistant City Attorney", value=[member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=city_attorney) and discord.utils.get(member.roles, id=moderator)][0], inline=False)
        else:
            embed.add_field(name="Assistant City Attorneys", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=city_attorney) and discord.utils.get(member.roles, id=moderator)]), inline=False)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="complaint", description="Submit a complaint against a member of the Redwood City Government.")
    @app_commands.guild_only()
    async def complaint(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ComplaintModal())
        pass

    pass

async def setup(bot):
    await bot.add_cog(LegalOfficeCog(bot))