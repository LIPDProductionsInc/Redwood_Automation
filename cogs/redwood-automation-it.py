import discord
import datetime
import sys
import traceback

from discord.ext import commands
from discord import app_commands

class RedwoodAutomationTicketModal(discord.ui.Modal, title="City Hall Ticket Submission"):
    type = discord.ui.TextInput(
        label="What type of issue are you having?",
        style=discord.TextStyle.short,
        placeholder="Bot Bug Report, Game Bug Report, Automation Bug Report, etc.",
        required=True
    )

    issue = discord.ui.TextInput(
        label="What is the issue?",
        style=discord.TextStyle.long,
        placeholder="Describe the issue you are having",
        required=True
    )

    urgent = discord.ui.TextInput(
        label="Is this issue interfering with your ability to do your job/operation?",
        style=discord.TextStyle.short,
        placeholder="Yes/No",
        min_length=2,
        max_length=3,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(1118048392698937376)
        embed = discord.Embed(
            title="City Hall Ticket Submission",
            colour=discord.Colour.dark_blue()
        )
        embed.add_field(name="Type", value=self.type.value, inline=True)
        embed.add_field(name="Issue", value=self.issue.value, inline=True)
        embed.add_field(name="Urgent", value=self.urgent.value, inline=True)
        embed.add_field(name="Submitted By", value=interaction.user.mention, inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by: {self.bot.owner}")
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        await interaction.response.send_message("Your ticket has been submitted!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("An error occurred while processing your ticket. Please try again later.", ephemeral=True)
        print('Ignoring exception in modal CityHallTicketModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        pass

    pass

class RedwoodAutomationITCog(commands.Cog, name="IT Commands"):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="ticket", description="Submit a ticket to the IT department")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(646549330479546379, 646549329493884929, 763470466269577216, 940718179402006590, 1004462014044831845)
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RedwoodAutomationTicketModal())
        pass

    pass

async def setup(bot):
    await bot.add_cog(RedwoodAutomationITCog(bot))