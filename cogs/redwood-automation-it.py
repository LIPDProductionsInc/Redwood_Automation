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
        label="Are you able to do your duties without this?",
        style=discord.TextStyle.short,
        placeholder="Yes/No",
        min_length=2,
        max_length=3,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel = interaction.client.get_channel(1154236870381805578)
        if self.urgent.value.lower() == "yes":
            self.urgent.value = "No"
        elif self.urgent.value.lower() == "no":
            self.urgent.value = "Yes"
        else:
            raise commands.BadArgument("Invalid argument for urgent")
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

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message("An error occurred while processing your ticket. Please try again later.", ephemeral=True)
        print('Ignoring exception in modal CityHallTicketModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        pass

    pass

class RedwoodAutomationITCog(commands.Cog, name="IT Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="ticket", description="Submit a ticket to the IT department")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1150770058935681162, 1150770058935681161, 1150770058935681160, 1150770058914705536, 1150770058914705533, 1150770058914705528, 1150770058897920159, 1150770058897920158, 1150770058897920157, 1150770058897920156, 1150770058881155123, 1005948844791574568)
    async def ticket(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RedwoodAutomationTicketModal())
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RedwoodAutomationITCog(bot))