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
    async def council(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Redwood City Council",
            description="Here is a list of the current city council members:",
            color=discord.Color.dark_blue()
            )
        guild = ctx.bot.get_guild(1150770058847588492) # Redwood City Discord Server
        embed.add_field(name="Mayor", value=guild.get_role(1150770058935681162).members[0].mention if len(ctx.guild.get_role(1150770058935681162).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="Deputy Mayor", value=guild.get_role(1150770058935681160).members[0].mention if len(ctx.guild.get_role(1150770058935681160).members) > 0 else "VACANT", inline=True)
        embed.add_field(name="Council Chairperson", value=guild.get_role(1150770058914705534).members[0].mention if len(ctx.guild.get_role(1150770058914705534).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="City Council Members", value="\n".join([member.mention for member in guild.members if discord.utils.get(member.roles, id=1150770058914705533) and not discord.utils.get(member.roles, id=1150770058914705534)]), inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="docket", description="Has the bot announce the next item on the city council docket.")
    @app_commands.guilds(1150770058847588492) # Redwood City Discord Server
    @app_commands.checks.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(first="True or False: This is the first item on the docket for the session.", docket_item = "The name of the item on the docket.", docket_link = "The Trello link to the item on the docket.", debate = "Is the floor open or closed for debate?")
    async def docket(self, interaction:discord.Interaction, first:Literal["True", "False"], docket_item:str, docket_link:str, debate:Literal["Open", "Closed"]) -> None:
        if interaction.channel.name.startswith("council-session"):
            if docket_link.startswith("https://trello.com/c/"):
                if first == "True":
                    message = f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n"
                    if debate == "Closed":
                        message += "(<@&1150770058914705533>)"
                    elif debate == "Open":
                        message += "Floor is open for debate. Say \"I\" to be recognized. (<@&1150770058914705533>)"
                    else:
                        raise ValueError(f"{debate} is not a valid value for debate.")
                else:
                    message = f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n"
                    if debate == "Closed":
                        message += "(<@&1150770058914705533>)"
                    elif debate == "Open":
                        message += "Floor is open for debate. Say \"I\" to be recognized. (<@&1150770058914705533>)"
                    else:
                        raise ValueError(f"{debate} is not a valid value for debate.")
                await interaction.response.send_message(f"{message}")
            else:
                await interaction.response.send_message(":x: The link you provided is not a valid Trello link. Please try again.", ephemeral=True)
            pass
        pass

    @commands.hybrid_command(name="session", description="Starts a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(session_type="The type of session to start. Either \"in-game\" or \"discord\".", session_number="The number of the Discord session.")
    async def session(self, ctx:commands.Context, session_type:Literal["In-Game", "Discord"], session_number:int = None) -> None:
        channel = ctx.bot.get_channel(1151380671126839386) # City Announcements
        if session_type == "In-Game":
            await channel.send(f"<:NewRedwoodSeal:1068175383729537065> | **SESSION**\n\n A City Council Session is starting in V2. Come on down to the City Hall located at the corner of 98th Ave and 100th Ave, down the street from the gas station.\n\nMake sure to park in the green area. Do not park in the red.\n\n@here",file=discord.File("/home/pi/Documents/Redwood_Automation/media/redwood-session-parking.jpg"))
        elif session_type == "Discord":
            overwrites = {
                ctx.guild.get_role(1150770058935681162): discord.PermissionOverwrite(send_messages=True), # Mayor
                ctx.guild.get_role(1150770058935681160): discord.PermissionOverwrite(send_messages=True), # Deputy Mayor
                ctx.guild.get_role(1150770058914705534): discord.PermissionOverwrite(send_messages=True), # Council Chairperson
                ctx.guild.get_role(1150770058914705533): discord.PermissionOverwrite(send_messages=True, add_reactions=True), # City Council
                ctx.guild.get_role(1150770058847588500): discord.PermissionOverwrite(view_channel=True, send_messages=False), # Redwood Citizens
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, add_reactions=False) # @everyone
            }
            if session_number is None:
                session_number = "new"
            channel2 = await ctx.guild.create_text_channel(f"council-session-{session_number}", category=ctx.guild.get_channel(1150770059933913192), overwrites=overwrites, reason="City Council Session Started")
            await channel.send(f"**A Discord City Council Session is starting.**\n\n{channel2.mention} \n\n@here")
            await channel2.send(f"<:NewRedwoodSeal:1154226637114708019> {ctx.author.mention} has called the council into order on this {datetime.datetime.now().strftime('%A, %B %d, %Y')} at {datetime.datetime.now().strftime('%I:%M %p')}.To declare presence, please state **\"I\"**. The session will commence upon the presence of 1/2 of the incumbent Alderpersons.\n\nIt is requested that you refrain from deleting or edit messages in order to prevent errors with the record of fact.\n\n(<@&1150770058914705533>)")
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="end-session", description="Ends a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(session_type="The type of session to end. Either \"in-game\" or \"discord\".")
    async def end_session(self, ctx:commands.Context, session_type:Literal["In-Game", "Discord"]) -> None:
        if session_type == "Discord":
            if ctx.channel.name.startswith("council-session"):
                channel = ctx.bot.get_channel(1150770060684705812) # City Clerk Channel
                await ctx.send("The session is hereby adjourned. \n\n (<@&1150770058914705533>)")
                overwrites = {
                    ctx.guild.get_role(1150770058935681157): discord.PermissionOverwrite(send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False), # Muted
                    ctx.guild.get_role(1150770058897920157): discord.PermissionOverwrite(send_messages=True), # City Clerk
                    ctx.guild.get_role(1150770058847588500): discord.PermissionOverwrite(view_channel=True, send_messages=False), # Redwood Citizens
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, add_reactions=False, send_messages=False) # @everyone
                }
                await ctx.channel.edit(category=ctx.guild.get_channel(761730715024097311), reason="Session Ended", position=0)
                await channel.send(f"<@&1150770058897920157>\n\nHi, the session in {ctx.channel.mention} has been adjourned and is awaiting transcribing!")
            else:
                if ctx.interaction == None:
                    await ctx.message.delete()
                raise commands.UserInputError("This command can only be used in a council session channel.")
        elif session_type == "In-Game":
            channel = ctx.bot.get_channel(1151380671126839386) # City Announcements
            await channel.send("The session has been adjourned.")
            pass
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="floor", description="Gives a non-council member the floor to speak.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(member="The non-council member to give the floor to.")
    async def floor(self, ctx:commands.Context, member:discord.Member) -> None:
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=1150770058935681162) or discord.utils.get(member.roles, id=1150770058935681160) or discord.utils.get(member.roles, id=1150770058914705534) or discord.utils.get(member.roles, id=1150770058914705533): # If the member is the Mayor, Deputy Mayor, Council Chairperson, or a City Council Member
                raise commands.BadArgument("This person can already speak in the session.")
            else:
                overwrite = discord.PermissionOverwrite(send_messages=True, embed_links=True)
                await ctx.channel.set_permissions(member, overwrite=overwrite)
                channel = ctx.bot.get_channel(1154236098525012008) # PO Logs
                embed = discord.Embed(
                    title="Floor Given",
                    colour=discord.Color.dark_blue()
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                embed.add_field(name="Floor Given To:", value=member.mention, inline=False)
                embed.add_field(name="Given By:", value=ctx.author.mention, inline=False)
                embed.set_footer(text=f"ID: {ctx.author.id}")
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
                await ctx.send(f"{member.mention}: you have the floor.")
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("The floor can only be given in a city council session channel.")
            pass
        pass

    @commands.hybrid_command(name="dismiss", description="Dismisses a non-council member from the floor.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(member="The non-council member to dismiss from the floor.")
    async def dismiss(self, ctx:commands.Context, member:discord.Member) -> None:
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=1150770058935681162) or discord.utils.get(member.roles, id=1150770058935681160) or discord.utils.get(member.roles, id=1150770058914705534) or discord.utils.get(member.roles, id=1150770058914705533): # If the member is the Mayor, Deputy Mayor, Council Chairperson, or a City Council Member
                raise commands.BadArgument("This person cannot be dismissed like this in the session.")
            else:
                await ctx.channel.set_permissions(member, overwrite=None)
                channel = ctx.bot.get_channel(1154236098525012008) # PO Logs
                embed = discord.Embed(
                    title="Dismissed From Floor",
                    colour=discord.Color.dark_blue()
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                embed.add_field(name="User Dismissed:", value=member.mention, inline=False)
                embed.add_field(name="Dismissed By:", value=ctx.author.mention, inline=False)
                embed.set_footer(text=f"ID: {ctx.author.id}")
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
                await ctx.send(f"{member.mention} has been dismissed from the floor.", ephemeral=True)
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("This command can only be used in a council session channel.")
            pass
        pass

    @commands.hybrid_command(name="propose", description="Proposes a bill to the rest of city council.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534, 1150770058914705533) # Mayor, Deputy Mayor, Council Chairperson, City Council
    @app_commands.describe(bill_name="The name of the bill bring proposed.", bill_link="The link to the bill being proposed.")
    async def propose(self, ctx:commands.Context, *, bill_name:str, bill_link:str) -> None:
        if ctx.channel.id == 1150770059933913195: # Legislation Proposal Channel
            if ctx.interaction == None:
                await ctx.message.delete()
            await ctx.send(f"**{ctx.author.mention}** has proposed a bill and is looking for co-sponsors. \n\n**Bill Name:** \"{bill_name}\" \n\n**Bill Link:** {bill_link} \n\nIf you would like to co-sponsor this bill, please respond with \"Support\" or \"Sponsor\" @here.")
        else:
            raise commands.UserInputError("This command can only be used in <#1150770059933913195>.")
            pass
    
    @commands.hybrid_command(name="legal-review", description="Send a proposal to the City Attorney's Office for review.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534, 1150770058914705533) # Mayor, Deputy Mayor, Council Chairperson, City Council
    @app_commands.describe(trello_link="The link to the Trello card for the proposal.")
    async def legal_review(self, ctx:commands.Context, trello_link:str) -> None:
        if ctx.interaction == None:
            await ctx.message.delete()
        if ctx.channel.id == 1150770059933913195: # Legislation Proposal Channel
            if trello_link.startswith("https://trello.com/c/"):
                channel = ctx.bot.get_channel(1150770061146067074) # City Attorney's Channel
                await channel.send(f"{trello_link}\n\n<@&1150770058914705528>\n\nSent by: {ctx.author.mention}")
                await ctx.send("The proposal has been sent to the City Attorney's Office for review.", ephemeral=True)
            else:
                raise commands.BadArgument("The link provided needs to be a Trello card.")
        else:
            raise commands.UserInputError("This command can only be used in <#1150770059933913195>.")
            pass
        pass

    @commands.hybrid_command(name="send", description="Send a proposal to either the mayor for signature or the persiding officer for notification.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534, 1150770058914705528) # Mayor, Deputy Mayor, Council Chairperson, City Clerk
    @app_commands.describe(trello_link="The link to the Trello card for the proposal.", location="The location to send the proposal to.")
    async def send(self, ctx:commands.Context, location: Literal["Mayor", "Docket"], trello_link:str) -> None:
        if location == "Mayor":
            if ctx.interaction == None:
                await ctx.message.delete()
            channel = self.bot.get_channel(1150770061146067065) # Mayor's Office
            if ctx.channel.name.startswith("council-session"):
                if trello_link.startswith("https://trello.com/c/"):
                    if len(ctx.guild.get_role(1249538789651517511).members) > 0: # If there's an Acting Mayor
                        ping = "<@&1249538789651517511>" # Ping the Acting Mayor
                    else:
                        ping = "<@&1150770058935681162>" # Ping the Mayor
                    await channel.send(f"{trello_link} \n\n{ping}")
                    await ctx.send("The bill has been sent to the mayor's office for signature.")
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            elif ctx.channel.id == 1150770059933913196: # If in the PO Channel
                if trello_link.startswith("https://trello.com/c/"):
                    if len(ctx.guild.get_role(1249538789651517511).members) > 0: # And there's an Acting Mayor
                        ping = "<@&1249538789651517511>" # Ping the Acting Mayor
                    else:
                        ping = "<@&1150770058935681162>" # Ping the Mayor
                    await channel.send(f"{trello_link} \n\n{ping}")
                    await ctx.send("Proposal sent to the mayor's office for signature.", ephemeral=True)
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            else:
                raise commands.UserInputError("This command can only be used in <#1150770059933913196> or a council session channel.")
                pass
        elif location == "Docket":
            if discord.utils.get(ctx.author.roles, id=1150770058914705528): # If the user is a City Attorney
                if ctx.channel.id == 1150770061146067074: # City Attorney's Channel
                    if ctx.interaction == None:
                        await ctx.message.delete()
                    channel = ctx.bot.get_channel(1150770059933913196) # Presiding Officer Channel
                    if trello_link.startswith("https://trello.com/c/"):
                        await channel.send(f"{trello_link} \n\n<@&1150770058914705534> Approved and added to the docket.")
                        await ctx.send("Presiding officer notified.", ephemeral=True)
                    else:
                        raise commands.BadArgument("The link provided needs to be a Trello card.")
                else:
                    raise commands.UserInputError("This command can only be used in <#1150770061146067074>.")
            else:
                await ctx.send("Wrong location to send the proposal to. Send to the Mayor, it's already on the docket.", ephemeral=True)
        else:
            raise commands.BadArgument("The location provided needs to be either Mayor or Docket.")
            pass
        pass

    @commands.hybrid_command(name="vote", description="Has the City Council start a vote")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534) # Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(type="The type of vote to start.")
    async def vote(self, ctx:commands.Context, type:Literal["Amendment", "Bill", "Motion", "Nomination", "Ratification", "Resolution"]) -> None:
        if ctx.channel.name.startswith("council-session"):
            if type != "Motion":
                if ctx.interaction == None:
                    await ctx.message.delete()
                    embed = discord.Embed(
                        description=f"**Vote on the {type.lower()}**",
                        colour=discord.Color.dark_blue()
                    )
                    embed.set_footer(text=f'Vote started by {ctx.author.display_name}', icon_url=ctx.author.avatar)
                    await ctx.send("<@&1150770058914705533>", embed=embed, reference=ctx.message.reference)
                else:
                    await ctx.send(f"Vote on the {type.lower()}\n\n<@&1150770058914705533>")
            else:
                if ctx.interaction == None:
                    embed = discord.Embed(
                        description=f"**Vote on the {type.lower()}**",
                        colour=discord.Color.dark_blue()
                    )
                    embed.set_footer(text=f'Vote started by {ctx.author.display_name}', icon_url=ctx.author.avatar)
                    await ctx.send("<@&1150770058914705533>", embed=embed)
                else:
                    await ctx.send(f"Vote on the {type.lower()}\n\n<@&1150770058914705533>")
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
            pass
        pass

    @commands.hybrid_command(name="charter", description="Sends a link to the City Charter.")
    @commands.guild_only()
    async def charter(self, ctx:commands.Context) -> None:
        if discord.utils.get(ctx.author.roles, id=1150770058935681162) or discord.utils.get(ctx.author.roles, id=1150770058935681160) or discord.utils.get(ctx.author.roles, id=1150770058914705534) or discord.utils.get(ctx.author.roles, id=1150770058914705533): # Mayor, Deputy Mayor, Council Chairperson, City Council
            await ctx.send("Here is the link to the Charter: (Where you can also make a copy for revisions/request edit access. Make sure to provide reasoning.) \n<https://docs.google.com/document/d/198OcRUF1Nbd9G1QrxvLXPgtxwofkImTXTa47xh-0pww/edit?usp=sharing>", ephemeral=True)
        else:
            await ctx.send("Current City Charter: \n<https://drive.google.com/file/d/1Q6QzU6fZM6vZ8W8m9X9F1pOJl0v1hWkK/view?usp=sharing>")
            pass
        pass

    @commands.hybrid_command(name="template", description="Sends a link to the Trello card proposal template.")
    @commands.guild_only()
    @commands.has_any_role(1150770058935681162, 1150770058935681160, 1150770058914705534, 1150770058914705533) # Mayor, Deputy Mayor, Council Chairperson, City Council
    async def template(self, ctx:commands.Context) -> None:
        await ctx.send("Here is the link to the Bill Templates: \n <https://trello.com/c/tuOk4RtM>")
        pass

    pass

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(CouncilCog(bot))
