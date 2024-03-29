import discord
import datetime

from discord import app_commands
from discord.ext import commands

class CityHallCog(commands.Cog, name="City Hall Related Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="documents", description="Get the required documents for your role.")
    @commands.guild_only()
    @commands.check_any(commands.has_any_role(1150770058897920157, 1150770058881155120, 1150770058897920159, 1150770058897920158, 1150770058914705534, 1150770058914705533, 1150770058935681160, 1150770058935681162))
    async def _documents(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title=f"List of Documents for {ctx.author.display_name}",
            colour=discord.Color.dark_blue()
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        embed.timestamp = datetime.datetime.now()
        if isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058897920157):
            embed.add_field(name="City Clerk:", value="https://docs.google.com/forms/d/1nGY6J8sF0xyqxW-nZBa9bnvydxnmO25KedYAXmG4_fI/edit \nhttps://docs.google.com/document/d/1Or8zmjojgLhp_E4JgybehFBhzsIy0eh1NbfzciPAWsc/edit \nhttps://docs.google.com/document/d/1V9T3kTvkNAhcc05boIkBu7gLN-6lwwxIvvx30x4j67k/edit?usp=sharing", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058881155120) or ctx.author.get_role(1005948844791574568):
            embed.add_field(name="Police Department:", value="Criminal Code: https://trello.com/b/EGN3OQzQ/firestone-criminal-code-r \nTraffic Regulations: https://trello.com/b/z1e04kAy/traffic-regulations-firestone \nCounty & Municipal Guide: https://trello.com/b/UhRYTqfo/firestone-county-municipal-legal-guide \nMedical Certs: https://trello.com/b/XnYh2AN1/state-registry-of-health \nWarrants: https://trello.com/b/KHYhrBju/district-court-of-firestone \nHandicap Permits: https://trello.com/b/vR54Te0o/fdot-handicap-permits-board \nHandbook: https://docs.google.com/document/d/18K-IHoT6MStN6b_kb7RSBGEpxMuSYgepN21Fw4TFtR0/edit", inline=False)
        #elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058897920159):
        #    embed.add_field(name="Press Secretary:", value="", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058897920158):
            embed.add_field(name="Office of Commerce Relations:", value="Trello Board: https://trello.com/b/ePQVqR70", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058914705534):
            embed.add_field(name="Council Chairperson:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058914705533):
            embed.add_field(name="Council Member:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058935681160):
            embed.add_field(name="Deputy Mayor:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ \n Mayor Office Board: https://trello.com/b/pK66sdV7", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1150770058935681162):
            embed.add_field(name="Mayor:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ \n Mayor Office Board: https://trello.com/b/pK66sdV7", inline=False)
        await ctx.send(embed=embed, ephemeral=True)
        pass

    @app_commands.command(name="announce", description="Send a message to the #announcements channel, with the option to auto-publish.")
    @app_commands.guild_only()
    @app_commands.guilds(1150770058847588492)
    @commands.check_any(commands.has_any_role(1150770058914705536, 1150770058914705534), commands.is_owner())
    @app_commands.describe(message="The message to send to #announcements.", publish="Whether or not to publish the message.")
    async def _publish(self, interaction: discord.Interaction, message: str, publish: bool) -> None:
        channel = self.bot.get_channel(1151380671126839386)
        if channel.permissions_for(interaction.user).send_messages:
            message = await channel.send(message)
            if publish:
                await message.publish()
        else:
            raise commands.MissingPermissions(["send_messages"])
        pass

    @commands.hybrid_command(name="epoch", description="Transform a date and time into Epoch time.")
    @commands.guild_only()
    @app_commands.describe(date="The date to convert.", time="The time to convert.")
    async def _epoch(self, ctx: commands.Context, date: str, time: str):
        date = date.split("/")
        time = time.split(":")
        date = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]))
        await ctx.send(f"Epoch time: {int(date.timestamp())}")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CityHallCog(bot))
