import discord
import datetime

from discord import app_commands
from discord.ext import commands
from datetime import timedelta
from typing import Literal

class CouncilCog(commands.Cog, name="Council Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="council", description="Shows the current city council members.")
    @commands.guild_only()
    async def council(self, ctx):
        embed = discord.Embed(
            title="Redwood City Council",
            description="Here is a list of the current city council members:",
            color=discord.Color.dark_blue()
            )
        embed.add_field(name="Mayor", value=ctx.guild.get_role(646549322682466305).members[0].mention if len(ctx.guild.get_role(646549322682466305).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="Deputy Mayor", value=ctx.guild.get_role(646551227626160139).members[0].mention if len(ctx.guild.get_role(646551227626160139).members) > 0 else "VACANT", inline=True)
        embed.add_field(name="Council Chairperson", value=ctx.guild.get_role(673008336010084378).members[0].mention if len(ctx.guild.get_role(673008336010084378).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="City Council Members", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549329493884929)]), inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="docket", description="Has the bot announce the next item on the city council docket.")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(first="True of False: This is the first item on the docket for the session.", docket_item = "The name of the item on the docket.", docket_link = "The Trello link to the item on the docket.")
    async def docket(self, interaction:discord.Interaction, first:Literal["True", "False"], docket_item:str, docket_link:str):
        if self.bot.channel.name.startswith("council-session"):
            if first == "True":
                await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
            else:
                await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
            pass
        pass

    @commands.hybrid_command(name="session", description="Starts a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(session_type="The type of session to start. Either \"in-game\" or \"discord\".")
    async def session(self, ctx, session_type:Literal["In-Game", "Discord"]):
        if session_type == "In-Game":
            channel = ctx.bot.get_channel(646541531523710996)
            await channel.send(f"**An in-game City Council Session is starting.**\n\nPlease join at the following link: <Link Here> \n\n@here")
        elif session_type == "Discord":
            overwrite = {
                ctx.guild.get_role(646549322682466305): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(646551227626160139): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(673008336010084378): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(646549329493884929): discord.PermissionOverwrite(send_messages=True)
            }
            await ctx.guild.create_text_channel(f"council-session-new", category=ctx.guild.get_channel(646552329654370345), overwrites=overwrite)
            await ctx.send(f"**A Discord City Council Session is starting.**\n\nPlease join at the following link: <Link Here> \n\n@here")
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="end-session", description="Ends a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(session_type="The type of session to end. Either \"in-game\" or \"discord\".")
    async def end_session(self, ctx, session_type:Literal["In-Game", "Discord"]):
        if session_type == "Discord":
            if ctx.channel.name.startswith("council-session"):
                await ctx.channel.category.edit(id=761730715024097311, reason="Session Ended", sync_permissions=True, position=0)
                await ctx.send("The session has been ended.")
            else:
                if ctx.interaction == None:
                    await ctx.message.delete()
                raise commands.UserInputError("This command can only be used in a council session channel.")
        elif session_type == "In-Game":
            channel = ctx.bot.get_channel(646541531523710996)
            await channel.send("The session has been ended.")
            pass
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="floor", description="Gives a non-council member the floor to speak.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(member="The non-council member to give the floor to.")
    async def floor(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=646549322682466305) or discord.utils.get(member.roles, id=646551227626160139) or discord.utils.get(member.roles, id=673008336010084378) or discord.utils.get(member.roles, id=646549329493884929):
                raise commands.BadArgument("This person can already speak in the session.")
            else:
                overwrite = {
                    member: discord.PermissionOverwrite(send_messages=True, embed_links=True)
                }
                await ctx.channel.edit(overwrites=overwrite)
                await ctx.send(f"{member.mention}: you have the floor.")
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("The floor can only be given in a city council session channel.")
            pass
        pass

    @commands.hybrid_command(name="dismiss", description="Dismisses a non-council member from the floor.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(member="The non-council member to dismiss from the floor.")
    async def dismiss(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=646549322682466305) or discord.utils.get(member.roles, id=646551227626160139) or discord.utils.get(member.roles, id=673008336010084378) or discord.utils.get(member.roles, id=646549329493884929):
                raise commands.BadArgument("This person cannot be dismissed like this in the session.")
            else:
                overwrite = {
                    member: discord.PermissionOverwrite(send_messages=False, embed_links=False)
                }
                await ctx.channel.edit(overwrites=overwrite)
                await ctx.send(f"{member.mention} has been dismissed from the floor.", ephemeral=True)
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("This command can only be used in a council session channel.")
            pass
        pass

    @commands.hybrid_command(name="propose", description="Proposes a bill to the rest of city council.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378, 646549329493884929)
    @app_commands.describe(bill_name="The name of the bill bring proposed.", bill_link="The link to the bill being proposed.")
    async def propose(self, ctx, *, bill_name, bill_link):
        if ctx.channel.id == 941499579029913611:
            if ctx.interaction == None:
                await ctx.message.delete()
            await ctx.send(f"**{ctx.author.mention}** has proposed a bill and is looking for co-sponsors. \n\n**Bill Name:** {bill_name} \n\n**Bill Link:** {bill_link} \n\nIf you would like to co-sponsor this bill, please respond with \"Support\" or \"Sponsor\" @here.")
        else:
            raise commands.UserInputError("This command can only be used in <#941499579029913611>.")
            pass
    
    @commands.hybrid_command(name="legal-review", description="Send a bill to the City Attorney's Office for review.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378, 646549329493884929)
    @app_commands.describe(trello_link="The link to the Trello card for the bill.")
    async def legal_review(self, ctx, trello_link):
        if ctx.interaction == None:
            await ctx.message.delete()
        if ctx.channel.id == 941499579029913611:
            if trello_link.startswith("https://trello.com/c/"):
                await ctx.send(f"{trello_link} \n\n <@&646549330479546379>")
            else:
                raise commands.BadArgument("The link provided needs to be a Trello card.")
        else:
            await ctx.send("This command can only be used in a council session channel.")
            pass
        pass

    @commands.hybrid_command(name="charter", description="Sends a link to the City Charter.")
    @commands.guild_only()
    async def charter(self, ctx):
        """If the member is part of the City Council, send them to the Google Docs link, otherwise send them to the Google PDF link"""
        if ctx.author.id in [646549322682466305, 646551227626160139, 673008336010084378, 646549329493884929]:
            await ctx.send("Here is the link to the Charter: (Where you can also make a copy for revisions/request edit access. Make sure to provide reasoning.) \n <https://docs.google.com/document/d/198OcRUF1Nbd9G1QrxvLXPgtxwofkImTXTa47xh-0pww/edit?usp=sharing>", ephemeral=True)
        else:
            await ctx.send("Current City Charter: \n <https://drive.google.com/file/d/1Q6QzU6fZM6vZ8W8m9X9F1pOJl0v1hWkK/view?usp=sharing>")
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))
