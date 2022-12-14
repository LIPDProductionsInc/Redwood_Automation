import discord
import datetime
import sys
import traceback

from discord import app_commands
from discord.ext import commands

class FeedbackModal(discord.ui.Modal, title="Feedback"):

    feedback = discord.ui.TextInput(
        label="Leave your feedback for the City of Redwood",
        style=discord.TextStyle.long,
        placeholder="Type your feedback here...",
        required=True,
        min_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you for your feedback!", ephemeral=True)
        channel = interaction.client.get_channel(1042645528053284874)
        embed = discord.Embed(
            title="New Feedback", 
            description=self.feedback.value, 
            colour=discord.Color.dark_blue()
            )
        embed.set_footer(text=f"ID: {interaction.user.id}")
        '''Get the bot's avatar via interaction and set it as the embed's thumbnail'''
        embed.set_thumbnail(url=interaction.guild.me.avatar)
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("An error occurred while processing this interaction.", ephemeral=True)
        print('Ignoring exception in modal FeedbackModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

class FeedbackCog(commands.Cog, name="Feedback"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Send feedback to the City of Redwood")
    @app_commands.guild_only()
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FeedbackModal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FeedbackCog(bot))