import discord
import datetime

from discord import app_commands
from discord.ext import commands

class POIDContextMenuCog(commands.Cog, name="POID Context Menu"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name='Get POID on This Message', callback=self.context_menu_callback))

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        embed = discord.Embed(
            title=f"POID for Message {message.id}",
            description=f"Message Content:\n{message.content[:1024]}",  # Limit content to 1024 characters
            type="rich",
            color=discord.Color.blue()
        )
        embed.add_field(name="Author", value=f"{message.author.mention} ({message.author.id})", inline=True)
        # Get when the message was sent and convert to epoch time for Discord's relative time display
        message_time = int(message.created_at.timestamp())
        embed.add_field(name="Message Sent At", value=f"<t:{message_time}:F> (<t:{message_time}:R>)", inline=True)
        embed.thumbnail(url=message.author.display_avatar.url)
        embed.set_author(name="Redwood Automation", icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.display_name} | ID: {interaction.user.id} | At:", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(POIDContextMenuCog(bot))