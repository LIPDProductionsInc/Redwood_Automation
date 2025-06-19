import discord
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
        if interaction.user.has_role(1150770058914705528):  # City Attorney role
            await interaction.response.send_message("Closing ticket...", ephemeral=True)
            await asyncio.sleep(2)  # Give time for the transcript to be sent
            await interaction.channel.delete()
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
        await ticket_creation_message.edit(content=f"Ticket created: {channel.mention}", view=None, embed=None)
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

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RedwoodAutomationFOIA(bot))
    pass
