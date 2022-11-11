import discord
import traceback

from discord import app_commands
from discord.ext import commands

class TestModal(discord.ui.Modal, title="Title"):
    feedback = discord.ui.TextInput(
        label='Label',
        style=discord.TextStyle.long,
        placeholder='Placeholder',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!')

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

class ContextTestCog(commands.Cog, name="Context Test Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name='Context Test', callback=self.context_menu_callback))

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.send_modal(TestModal())
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    bot.add_cog(ContextTestCog(bot))