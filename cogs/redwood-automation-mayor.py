import discord

from discord import app_commands
from discord.ext import commands

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
            if position.id == 646549322682466305:
                await ctx.send("You cannot appoint someone to the Mayor role!", ephemeral=True)
            elif position.id == 646551227626160139:
                if len(ctx.guild.get_role(646551227626160139).members) > 0:
                    await ctx.send("There is already a Deputy Mayor!", ephemeral=True)
                else:
                    channel = ctx.bot.get_channel(646541531523710996)
                    role = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                    await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been nominated as Deputy Mayor!")
                    await channel.send(f"<:NewMayorSeal:1033299735630585876> {person.mention} has been nominated as Deputy Mayor!\n\n- {ctx.author.mention}")
            elif position.id == 954794454026424370:
                channel = ctx.bot.get_channel(646541531523710996)
                role1 = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                role2 = discord.utils.get(ctx.guild.roles, id=763470466269577216)
                role3 = discord.utils.get(ctx.guild.roles, id=646554162405834762)
                role4 = discord.utils.get(ctx.guild.roles, id=1038941326047191161)
                await person.add_roles(role1, role2, role3, role4, reason=f"Appointed by {ctx.author} ({ctx.author.id})")
                await ctx.send(f"{person.mention} has been appointed as an Advisor!")
                await channel.send(f"<:NewMayorSeal:1033299735630585876> {person.mention} has been appointed as an Advisor!\n\n- {ctx.author.mention}")
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(646549322682466305) or ctx.author.get_role(646551227626160139): #Mayor or Deputy Mayor
            if position.id == 673008336010084378:
                if len(ctx.guild.get_role(673008336010084378).members) > 0:
                    await ctx.send("There is already a Chairperson!", ephemeral=True)
                else:
                    channel = ctx.bot.get_channel(646541531523710996)
                    role = discord.utils.get(ctx.guild.roles, id=763471193377603644)
                    await person.add_roles(role, reason=f"Nominated by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been nominated as Chairperson!")
                    await channel.send(f"<:NewMayorSeal:1033299735630585876> {person.mention} has been nominated as Chairperson!\n\n- {ctx.author.mention}")
            elif position.id == 646549329493884929:
                if len(ctx.guild.get_role(646549329493884929).members) > 5:
                    await ctx.send("There are already 6 members of the Council!", ephemeral=True)
                else:
                    role = discord.utils.get(ctx.guild.roles, id=851212299745230898)
                    await person.add_roles(role, reason=f"Added by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been added as an Alderperson-elect!")
            else:
                await ctx.send("You cannot appoint someone to that role at this time!", ephemeral=True)
        elif isinstance(ctx.author, discord.Member) and ctx.author.get_role(673008336010084378): #Chairperson
            if position.id == 646549329493884929:
                if len(ctx.guild.get_role(646549329493884929).members) > 5:
                    await ctx.send("There are already 6 members of the Council!", ephemeral=True)
                else:
                    role = discord.utils.get(ctx.guild.roles, id=851212299745230898)
                    await person.add_roles(role, reason=f"Added by {ctx.author} ({ctx.author.id})")
                    await ctx.send(f"{person.mention} has been added as an Alderperson-elect!")
            else:
                await ctx.send("You cannot appoint someone to that role!", ephemeral=True)

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))