import discord
import datetime

from discord.ext import commands
from discord import app_commands

class RedwoodAutomationOCR(commands.Cog, name="Office of Commerce Relations Commands"):
    def __init__(self, bot) -> None:
       self.bot = bot

    @commands.hybrid_command(name="business-representative", description="Register as a business representative with the Office of Commerce Relations.")
    @commands.guild_only()
    @app_commands.describe(permit_link="The DOCM Trello link for your business.")
    async def business_representative(self, ctx, *, permit_link: str):
        if permit_link.startswith("https://trello.com/c/"):
            channel = self.bot.get_channel(1005535705180672081)
            embed = discord.Embed(
                title="New Business Representative Role Request",
                type="rich",
                colour=discord.Colour.dark_blue()
            )
            embed.add_field(name="User", value=f"{ctx.author.mention}", inline=False)
            embed.add_field(name="Permit Link", value=f"{permit_link}", inline=False)
            embed.set_footer(text=f"Redwood Automation | Developed by: {self.bot.owner}")
            embed.set_thumbnail(url=str(self.bot.user.avatar))
            embed.timestamp = datetime.datetime.now()
            message = await channel.send("<@&941858937836302377>", embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await ctx.send("Your request has been sent to the Office of Commerce Relations. Your role will be added upon verification.", ephemeral=True)
        else:
            await ctx.send("That is an invalid permit link. Please use the DOCM Trello Board to find your business permit.", ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RedwoodAutomationOCR(bot))