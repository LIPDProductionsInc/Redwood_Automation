import discord
import datetime

from discord.ext import commands

class CityHallCog(commands.Cog, name="City Hall Related Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="documents", description="Get the required documents for your role.")
    @commands.guild_only()
    @commands.check_any(commands.has_any_role(763471193524535336, 1004462014044831845, 763471106618556416, 940718179402006590, 673008336010084378, 646549329493884929, 646551227626160139, 646549322682466305))
    async def _documents(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"List of Documents for {ctx.author.display_name}",
            colour=discord.Color.dark_blue()
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        embed.timestamp = datetime.datetime.now()
        if isinstance(ctx.author, discord.Member) and ctx.author.get_role(763471193524535336):
            embed.add_field(name="City Clerk:", value="https://docs.google.com/forms/d/1nGY6J8sF0xyqxW-nZBa9bnvydxnmO25KedYAXmG4_fI/edit \nhttps://docs.google.com/document/d/1Or8zmjojgLhp_E4JgybehFBhzsIy0eh1NbfzciPAWsc/edit", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(1004462014044831845):
            embed.add_field(name="Police Department:", value="Criminal Code: https://trello.com/b/EGN3OQzQ/firestone-criminal-code-r \nTraffic Regulations: https://trello.com/b/z1e04kAy/traffic-regulations-firestone \nCounty & Municipal Guide: https://trello.com/b/UhRYTqfo/firestone-county-municipal-legal-guide \nMedical Certs: https://trello.com/b/XnYh2AN1/state-registry-of-health \nWarrants: https://trello.com/b/KHYhrBju/district-court-of-firestone \nHandicap Permits: https://trello.com/b/vR54Te0o/fdot-handicap-permits-board \nHandbook: https://docs.google.com/document/d/18K-IHoT6MStN6b_kb7RSBGEpxMuSYgepN21Fw4TFtR0/edit", inline=False)
        #elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(763471106618556416):
        #    embed.add_field(name="Press Secretary:", value="", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(940718179402006590):
            embed.add_field(name="Office of Commerce Relations:", value="Trello Board: https://trello.com/b/ePQVqR70", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(673008336010084378):
            embed.add_field(name="Council Chairperson:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646549329493884929):
            embed.add_field(name="Council Member:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646551227626160139):
            embed.add_field(name="Deputy Mayor:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ \n Mayor Office Board: https://trello.com/b/pK66sdV7", inline=False)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646549322682466305):
            embed.add_field(name="Mayor:", value="Council Board: https://trello.com/b/gVPTVd0r \nRecords Board: https://trello.com/b/g06YwcHJ \n Mayor Office Board: https://trello.com/b/pK66sdV7", inline=False)
        await ctx.send(embed=embed, ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CityHallCog(bot))