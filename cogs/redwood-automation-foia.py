import discord
import asyncio
import chat_exporter
import io
import json
import typing

from discord import app_commands
from discord.ui import View
from discord.ext import commands
from typing import Literal

class CloseTicketButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.get_role(1150770058914705528):  # City Attorney Role
            channel = discord.utils.get(interaction.guild.channels, id=1385276524630118631)  # FOIA Tickets Archive Channel
            await interaction.response.send_message("Saving transcript...", ephemeral=True)
            try:
                message_count = 0
                async for _ in interaction.channel.history(limit=None):
                    message_count += 1
                transcript = await chat_exporter.export(interaction.channel, tz_info='EST', fancy_times=True, limit=message_count)
                transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"{interaction.channel.name}.html")
                await channel.send(f"{interaction.channel.name}", file=transcript_file)
                await interaction.response.send_message("Closing ticket...", ephemeral=True)
                await asyncio.sleep(2)  # Give time for the transcript to be sent
                await interaction.channel.delete()
            except Exception as e:
                await interaction.followup.send(f"Error saving transcript: {e}", ephemeral=True)
                print(f"Ignoring exception in CloseTicketButton callback: {e}")
                return
        else:
            await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
        pass

    pass

class FOIAButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()

    def get_next_ticket_number(self) -> int:
        with open("/home/pi/Documents/Redwood_Automation/db/foia-tickets.json", "r") as f:
            data = json.load(f)
        data["last_ticket_number"] += 1
        next_number = data["last_ticket_number"]

        with open("/home/pi/Documents/Redwood_Automation/db/foia-tickets.json", "w") as f:
            json.dump(data, f)

        return next_number

    @discord.ui.button(label="Open FOIA Ticket", style=discord.ButtonStyle.primary, custom_id="foia_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket_creation_message = await interaction.response.send_message("Opening ticket...", ephemeral=True)
        foiacategory = discord.utils.get(interaction.guild.categories, id=1384722375714537543)
        city_attorney = discord.utils.get(interaction.guild.roles, id=1150770058914705528)
        ticket_number = self.get_next_ticket_number()
        ticket_name = f"foia-request-{ticket_number:03}"
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            city_attorney: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await interaction.guild.create_text_channel(name=ticket_name, category=foiacategory, overwrites=overwrites)
        close_view = View()
        close_view.add_item(CloseTicketButton())
        ticket_embed = discord.Embed(
            title=f"FOIA Ticket #{ticket_number:03}",
            description="This is a ticket for FOIA requests. Please provide what you are requesting below.",
            color=discord.Color.blue()
        )
        ticket_embed.set_footer(text="The City Attorney's Office will respond to your request as soon as possible.")
        await channel.send(embed=ticket_embed, view=close_view)
        await interaction.reaction.edit_original_response(content=f"Ticket created: {channel.mention}")
        pass

    pass

class RedwoodAutomationFOIA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_owner(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 222766150767869952

    @app_commands.command(name="init-foia", description="Initialize the FOIA ticket system.")
    @app_commands.check(is_owner)
    @app_commands.guilds(1150770058847588492)  # Redwood City Discord Server
    async def init_foia(self, interaction: discord.Interaction) -> None:
        """Initialize the FOIA ticket system by creating the necessary category and button."""
        channel = discord.utils.get(interaction.guild.channels, id=1384043687784353915)
        embed = discord.Embed(
            title="Freedom of Information Act (FOIA) Request",
            description="Click the button below to create a FOIA request.",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed, view=FOIAButton())
        await interaction.response.send_message("FOIA ticket system initialized.", ephemeral=True)
        pass

    @app_commands.command(name="reset-ticket", description="Reset the tickeet counter")
    @app_commands.check(is_owner)
    @app_commands.guilds(1150770058847588492)  # Redwood City Discord Server
    async def reset_ticket(self, interaction: discord.Interaction) -> None:
        with open("/home/pi/Documents/Redwood_Automation/db/foia-tickets.json", "r") as f:
            data = json.load(f)
        data["last_ticket_number"] = 0
        with open("/home/pi/Documents/Redwood_Automation/db/foia-tickets.json", "w") as f:
            json.dump(data, f)
        await interaction.response.send_message("Ticket counter reset to 0.", ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RedwoodAutomationFOIA(bot))
    pass
