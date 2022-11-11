import discord

from discord import app_commands
from discord.ext import commands

class ContextTestCog(commands.Cog, name="Context Test Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name='Context Test', callback=self.context_menu_callback))

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.sendmessage('Context Test', ephemeral=True)
        await message.reply('Reply')
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ContextTestCog(bot))