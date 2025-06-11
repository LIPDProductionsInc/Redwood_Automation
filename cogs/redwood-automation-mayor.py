import discord
import typing

from discord import app_commands
from discord.ext import commands
from typing import Literal

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="elections", description="Announces the start of elections")
    @commands.has_any_role(1150770058935681163, 1150770058935681162, 1150770058935681160, 1150770058914705534) # County Executive, Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(type="The type of election to announce", forumlink="The link to the forum post")
    async def elections(self, ctx:commands.Context, type:Literal["Mayor and Deputy Mayor", "City Council", "City Council (Special)"], forumlink:str) -> None:
        if type == "Mayor and Deputy Mayor":
            if ctx.author.get_role(1150770058935681163): # County Executive
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(1151380671126839386) # Announcements channel
                    await channel.send(f"<:NewRedwoodSeal:1154226637114708019> | **MAYOR/DEPUTY MAYOR ELECTIONS**\n\nElections for Mayor and Deputy Mayor are now open! Check the details in the forum post below!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce Mayor and Deputy Mayor elections!")
        elif type == "City Council":
            if ctx.author.get_role(1150770058935681162) or ctx.author.get_role(1150770058935681160) or ctx.author.get_role(1150770058914705534): # Mayor, Deputy Mayor, Council Chairperson
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(1151380671126839386) # Announcements channel
                    await channel.send(f"<:NewRedwoodSeal:1154226637114708019> | **CITY COUNCIL ELECTIONS**\n\nElections for Redwood City Council are now open! Check the details in the forum post below, including how many seats are open!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce City Council elections!")
        elif type == "City Council (Special)":
            if ctx.author.get_role(1150770058935681162) or ctx.author.get_role(1150770058935681160) or ctx.author.get_role(1150770058914705534): # Mayor, Deputy Mayor, Council Chairperson
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(1151380671126839386) # Announcements channel
                    await channel.send(f"<:NewRedwoodSeal:1154226637114708019> | **CITY COUNCIL SPECIAL ELECTIONS**\n\nSpecial Elections for Redwood City Council are now open! Check the details in the forum post below, including how many seats are open!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce City Council elections!")
            pass
        pass

    @commands.hybrid_command(name="oaths", description="Begins the oath taking process for a new term")
    @app_commands.guilds(discord.Object(id=1150770058847588492)) # City of Redwood
    @commands.has_any_role(1150770058935681163, 1150770058935681162, 1150770058935681160, 1150770058914705534, 1154217793030471721) # County Executive, Mayor, Deputy Mayor, Council Chairperson
    @app_commands.describe(term_id="The ID of the term (Ie, '2023-3')")
    async def oaths(self, ctx:commands.Context, term_id:str) -> None:
        if ctx.guild.id != 1150770058847588492: # City of Redwood
            raise commands.UserInputError("This command can only be used in the City of Redwood!")
        channel = ctx.guild.get_channel(1382031974058823720) # Oaths channel
        async for message in channel.history(limit=100): # Check if there's a pinned message from the bot for the previous term
            if message.author == ctx.bot.user and message.pinned:
                if term_id in message.content: # Check if the message has the same term ID as the one provided by the user
                    raise commands.UserInputError(f"Oaths for term {term_id} have already been started!")
                else: # Otherwise, unpin the previous message
                    await message.unpin()
                break
        if channel is None:
            raise commands.UserInputError("The oaths channel could not be found!")
        newmessage = await channel.send(f"------------------\n\n<:NewRedwoodSeal:1154226637114708019> | **OATHS FOR TERM {term_id}**\n\nThe oaths for the {term_id} term can be found below. Please recite the oath to the person who is administering the oath. Do not edit your message after sending it to peserve the record of fact.")
        await newmessage.pin()
        await ctx.send(f"Oaths for term {term_id} have been started. Oaths can be found in Article 8 of the [City Charter](https://drive.google.com/file/d/1NyT5dix0r9-fkKsK0p6LKgctQds9a7La/view).", ephemeral=True)
        pass

    @commands.hybrid_command(name="seal", description="Updates the seal of the city")
    @app_commands.guilds(discord.Object(id=1150770058847588492)) # City of Redwood
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_any_role(1150770058897920159, 1150770058935681160, 1150770058935681160)) # Press Secretary, Deputy Mayor, Mayor
    @app_commands.describe(file="The PNG file to use as the seal")
    async def seal(self, ctx:commands.Context, file:discord.Attachment) -> None:
        if ctx.guild.id == 1150770058847588492:
            if file.filename.endswith(".png"):
                await ctx.guild.edit(icon=file.fp.read())
                await ctx.bot.user.edit(avatar=file.fp.read())
                await ctx.send("Seal updated!", ephemeral=True)
            else:
                raise commands.BadArgument("That is not a PNG file!")
        else:
            raise commands.UserInputError("This command can only be used in the City of Redwood!")
        pass

    @commands.hybrid_command(name="polls", description="Provides a link to approval polls")
    @commands.guild_only()
    async def polls(self, ctx:commands.Context) -> None:
        await ctx.send("https://forms.gle/fd3SC9hRV9yzaR8e7", ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))
