import discord
import asyncio

from discord import app_commands
from discord.ext import commands

class VoteOptions(discord.ui.Select):
    def __init__(self):
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
            description=f"**Vote on the {self.values[0].lower()}**",
            colour=discord.Color.dark_blue()
        )
        #embed.set_footer(text=f'Vote started by {interaction.author.display_name}', icon_url=interaction.author.avatar)
        self.voteoption = embed

class VoteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(VoteOptions())

class ContextTestCog(commands.Cog, name="Context Test Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.bot.tree.add_command(app_commands.ContextMenu(name='Context Test', callback=self.context_menu_callback))

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        view = VoteView()
        await interaction.response.send_message('Select the vote type below', view=view, ephemeral=True)
        await message.reply(embed=self.voteoptions)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ContextTestCog(bot))