import discord
import asyncio

from discord import app_commands
from discord.ext import commands

class VoteOptions(discord.ui.Select):
    def __init__(self, message: discord.Message):
        self.message = message
        options = [
            discord.SelectOption(label="Amendment", value="Has the council vote on the charter amendment proposal."),
            discord.SelectOption(label="Bill", value="Has the council vote on the bill proposal."),
            discord.SelectOption(label="Motion", value="Has the council vote on the motion."),
            discord.SelectOption(label="Nomination", value="Has the council vote on the nomination of a person to a position."),
            discord.SelectOption(label="Resolution", value="Has the council vote on the resolution.")
        ]

        super().__init__(placeholder="Select a vote type", options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
                description = f'**Vote on the {self.labels[0].lower()}**',
                colour=discord.Color.dark_blue()
            )
        embed.set_footer(text=f'Vote started by {interaction.user.display_name}', icon_url=interaction.user.avatar)
        await self.message.reply(embed=embed)

class VoteView(discord.ui.View):
    def __init__(self, message: discord.Message):
        super().__init__()
        self.add_item(VoteOptions(message))

class ContextTestCog(commands.Cog, name="Context Test Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name='Start a Vote', callback=self.context_menu_callback))

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if interaction.channel.name.startswith("council-session"):
            view = VoteView(message)
            await interaction.response.send_message('Select the vote type below', view=view, ephemeral=True)
        else:
            await interaction.response.send_message('This command can only be used in a council session channel.', ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ContextTestCog(bot))
