import discord
import typing

from discord import app_commands
from discord.ext import commands
from typing import Literal

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

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
                raise commands.BadArgument("You do not have permission to announce Mayor and Deputy Mayor elections!")
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
    @app_commands.describe(type="The type of oath channel to create", term_id="The ID of the term (Ie, '2023-3')")
    async def oaths(self, ctx:commands.Context, type:Literal["Mayor's Office", "City Council"], term_id:str) -> None:
        overwrites = {
            ctx.guild.get_role(851212299745230898): discord.PermissionOverwrite(send_messages=True),
            ctx.guild.get_role(763471193377603644): discord.PermissionOverwrite(send_messages=True),
            ctx.guild.get_role(763469321459728384): discord.PermissionOverwrite(view_channel=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False)
        }
        if type == "Mayor's Office":
            type = "mayors-office"
        elif type == "City Council":
            type = "city-council"
        await ctx.guild.create_text_channel(f"{type}-oaths-{term_id}", overwrites=overwrites)
        await ctx.send("Oaths channel created!", ephemeral=True)
        pass

    @commands.hybrid_command(name="seal", description="Updates the seal of the city")
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_any_role(987139446971432971, 646551227626160139, 763471106618556416))
    @app_commands.describe(file="The PNG file to use as the seal")
    async def seal(self, ctx:commands.Context, file:discord.Attachment) -> None:
        if ctx.guild.id == 646540220539338773:
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
