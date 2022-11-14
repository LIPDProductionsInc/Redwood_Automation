import discord
import traceback

from discord import app_commands
from discord.ext import commands

class ApprovalPoll(discord.ui.Modal, title="Title (This is a test)"):
    name = discord.ui.TextInput(
        label="Name Label", 
        placeholder="Placeholder Label"
        )
    
    feedback = discord.ui.TextInput(
        label="Feedback Label",
        style=discord.TextStyle.long,
        placeholder="Placeholder Label",
        required=False,
        max_length=300
    )

    button = discord.ui.Button(
        label="Button Label",
        style=discord.ButtonStyle.primary
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

    pass

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='feedback', description='Send feedback to the Mayor')
    @commands.guild_only()
    @commands.is_owner()
    async def feedback(self, interaction: discord.Interaction) -> None:
        channel = self.bot.get_channel(808055214287618059)
        await channel.response.send_modal(ApprovalPoll())

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))