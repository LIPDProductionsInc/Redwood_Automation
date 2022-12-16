import discord
import typing

from discord import app_commands
from discord.ext import commands
from typing import Literal

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="appoint", description="Appoints a person to a position")
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    @app_commands.describe(person="The person to appoint to the position", position="The position to appoint the person to")
    async def appoint(self, ctx: commands.Context, person: discord.Member, position: discord.Role) -> None:
        if isinstance(ctx.author, discord.Member) and ctx.author.top_role < position:
            await ctx.send("You cannot appoint someone to a position higher than your own!")
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646549322682466305): # Mayor only
            if position.id == 646549322682466305: #Mayor
                await ctx.send("You cannot appoint someone to the Mayor role!", ephemeral=True)
            elif position.id == 646551227626160139: #Deputy Mayor
                if len(ctx.guild.get_role(646551227626160139).members) > 0:
                    await ctx.send("There is already a Deputy Mayor!", ephemeral=True)
                else:
                    channel = ctx.bot.get_channel(646541531523710996)
                    role = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                    await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been nominated as Deputy Mayor!")
                    await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been nominated as Deputy Mayor!\n\n- {ctx.author.mention}")
            elif position.id == 954794454026424370: #Advisor
                channel = ctx.bot.get_channel(646541531523710996)
                role1 = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                role2 = discord.utils.get(ctx.guild.roles, id=763470466269577216)
                role3 = discord.utils.get(ctx.guild.roles, id=646554162405834762)
                role4 = discord.utils.get(ctx.guild.roles, id=1038941326047191161)
                await person.add_roles(role1, role2, role3, role4, reason=f"Appointed by {ctx.author} ({ctx.author.id})")
                await ctx.send(f"{person.mention} has been appointed as an Advisor!")
                await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been appointed as an Advisor!\n\n- {ctx.author.mention}")
            elif position.id == 673008336010084378: #Chairperson
                if len(ctx.guild.get_role(673008336010084378).members) > 0:
                    await ctx.send("There is already a Chairperson!", ephemeral=True)
                else:
                    channel = ctx.bot.get_channel(646541531523710996)
                    role = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                    await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been nominated as Chairperson!")
                    await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been nominated as Chairperson!\n\n- {ctx.author.mention}")
            elif position.id == 646549329493884929: #City Council
                if len(ctx.guild.get_role(646549329493884929).members) > 5:
                    await ctx.send("There are already 6 members of the Council!", ephemeral=True)
                else:
                    role = discord.utils.get(ctx.guild.roles, id=851212299745230898)
                    await person.add_roles(role, reason=f"Added by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been added as an Alderperson-elect!", ephemeral=True)
            elif position.id == 1038941326047191161: #Redwood Executive Emergency Committee
                channel = ctx.bot.get_channel(646541531523710996)
                role = discord.utils.get(ctx.guild.roles, id=1038941326047191161)
                await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                await ctx.send(f"{person.mention} has been appointed to the Redwood Executive Emergency Comittee!")
                await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been appointed to the Redwood Executive Emergency Comittee!\n\n- {ctx.author.mention}")
            else:
                await ctx.send("You cannot appoint someone to that role at this time!", ephemeral=True)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646551227626160139): #Deputy Mayor
            if position.id == 673008336010084378: #Chairperson
                if len(ctx.guild.get_role(673008336010084378).members) > 0:
                    await ctx.send("There is already a Chairperson!", ephemeral=True)
                else:
                    channel = ctx.bot.get_channel(646541531523710996)
                    role = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                    await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been nominated as Chairperson!")
                    await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been nominated as Chairperson!\n\n- {ctx.author.mention}")
            elif position.id == 646549329493884929: #City Council
                if len(ctx.guild.get_role(646549329493884929).members) > 5:
                    await ctx.send("There are already 6 members of the Council!", ephemeral=True)
                else:
                    role = discord.utils.get(ctx.guild.roles, id=851212299745230898)
                    await person.add_roles(role, reason=f"Added by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been added as an Alderperson-elect!", ephemeral=True)
            elif position.id == 987139446971432971: #Redwood Executive Emergency Committee
                channel = ctx.bot.get_channel(646541531523710996)
                role = discord.utils.get(ctx.guild.roles, id=987139446971432971)
                await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                await ctx.send(f"{person.mention} has been nominated as Chairperson!")
                await channel.send(f"<:NewMayorSeal:1033299735630585876> | {person.mention} has been appointed to the Redwood Executive Emergency Comittee!\n\n- {ctx.author.mention}")
            else:
                await ctx.send("You cannot appoint someone to that role at this time!", ephemeral=True)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(673008336010084378): #Chairperson
            if position.id == 646549329493884929: #City Council
                if len(ctx.guild.get_role(646549329493884929).members) > 5:
                    await ctx.send("There are already 6 members of the Council!", ephemeral=True)
                else:
                    role = discord.utils.get(ctx.guild.roles, id=851212299745230898)
                    await person.add_roles(role, reason=f"Added by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been added as an Alderperson-elect!")
            else:
                await ctx.send("You cannot appoint someone to that role!", ephemeral=True)
                pass
            pass
        pass

    @commands.hybrid_command(name="elections", description="Announces the start of elections")
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378, 646716958145904652)
    @app_commands.describe(type="The type of election to announce", forumlink="The link to the forum post")
    async def elections(self, ctx:commands.Context, type:Literal["Mayor and Deputy Mayor", "City Council", "City Council (Special)"], forumlink:str) -> None:
        if type == "Mayor and Deputy Mayor":
            if ctx.author.get_role(646716958145904652):
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(646541531523710996)
                    await channel.send(f"<:NewRedwoodSeal:1029041166508904519> | **MAYOR/DEPUTY MAYOR ELECTIONS**\n\nElections for Mayor and Deputy Mayor are now open! Check the details in the forum post below!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce Mayor and Deputy elections!")
        elif type == "City Council":
            if ctx.author.get_role(646549322682466305) or ctx.author.get_role(646551227626160139) or ctx.author.get_role(673008336010084378):
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(646541531523710996)
                    await channel.send(f"<:NewRedwoodSeal:1029041166508904519> | **CITY COUNCIL ELECTIONS**\n\nElections for Redwood City Council are now open! Check the details in the forum post below, including how many seats are open!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce City Council elections!")
        elif type == "City Council (Special)":
            if ctx.author.get_role(646549322682466305) or ctx.author.get_role(646551227626160139) or ctx.author.get_role(673008336010084378):
                if forumlink.startswith("https://forums.stateoffirestone.com/t/"):
                    channel = ctx.bot.get_channel(646541531523710996)
                    await channel.send(f"<:NewRedwoodSeal:1029041166508904519> | **CITY COUNCIL SPECIAL ELECTIONS**\n\nSpecial Elections for Redwood City Council are now open! Check the details in the forum post below, including how many seats are open!\n{forumlink}\n\n@everyone\n\n- {ctx.author.mention}")
                    await ctx.send("Elections have been announced!", ephemeral=True)
                else:
                    raise commands.BadArgument("That is not a valid link!")
            else:
                raise commands.BadArgument("You do not have permission to announce City Council elections!")
            pass
        pass

    @commands.hybrid_command(name="oaths", description="Creates a channel where people can take their oaths for the term")
    @commands.has_any_role(721013396094582795, 646549322682466305, 646551227626160139, 673008336010084378)
    async def oaths(self, ctx:commands.Context, type:Literal["Mayor's Office", "City Council"], term_id:str) -> None:
        overwrites = {
            ctx.guild.get_role(851212299745230898): discord.PermissionOverwrite(send_messages=True),
            ctx.guild.get_role(763471193377603644): discord.PermissionOverwrite(send_messages=True)
        }
        if type == "Mayor's Office":
            type = "mayors-office"
        elif type == "City Council":
            type = "city-council"
        await ctx.guild.create_text_channel(f"{type}-oaths-{term_id}", overwrites=overwrites)
        await ctx.send("Oaths channel created!", ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))
