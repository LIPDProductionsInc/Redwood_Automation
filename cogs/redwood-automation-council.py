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
        embed.add_field(name="Mayor", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549322682466305)}, inline=True)
        embed.add_field(name="Deputy Mayor", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646551227626160139)}, inline=True)
        embed.add_field(name="City Council Chairperson", value={member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=673008336010084378)}, inline=False)
        embed.add_field(name="City Council Members", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=646549329493884929)]), inline=True)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.avatar_url))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="docket", description="Has the bot announce the next item on the city council docket.")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    async def docket(self, interaction:discord.Interaction, first:Literal["True", "False"], docket_item:str, docket_link:str):
        if self.bot.category_id == 646552329654370345:
            if first == "True":
                await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
            else:
                await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\n Floor is open for debate. Say \"I\" to be recognized. (<@&646549329493884929>)")
        else:
            await interaction.response.send_message("The docket can only be announced in the city council channel.", ephemeral=True)
            pass
        pass

    @commands.hybrid_command(name="session", description="Starts a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    async def session(self, ctx, session_type:Literal["In-Game", "Discord"]):
        if session_type == "In-Game":
            await ctx.send(f"**An in-game City Council Session is starting.**\n\nPlease join at the following link: <Link Here> \n\n@here")
        elif session_type == "Discord":
            overwrite = {
                ctx.guild.get_role(646549322682466305): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(646551227626160139): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(673008336010084378): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(646549329493884929): discord.PermissionOverwrite(send_messages=True)
            }
            await ctx.guild.create_text_channel(f"council-session-new", category=ctx.guild.get_channel(646552329654370345), overwrites=overwrite)
            await ctx.send(f"**{ctx.author} has started a Discord city council session.**\n\nPlease join the session channel.")
        pass

    #@commands.hybrid_command(name="end-session", description="Ends a city council session, either in-game or on Discord.")
    #@commands.guild_only()
    #@commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    #Coming soon...

    @commands.hybrid_command(name="floor", description="Gives a non-council member the floor to speak.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    async def floor(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            overwrite = {
                member: discord.PermissionOverwrite(send_messages=True, embed_links=True)
            }
            await ctx.channel.edit(overwrites=overwrite)
            await ctx.send(f"{member.mention}: you have the floor.")
        else:
            await ctx.send("The floor can only be given in a city council session channel.")
            pass
        pass

    @commands.hybrid_command(name="dismiss", description="Dismisses a non-council member from the floor.")
    @commands.guild_only()
    @commands.has_any_role(646549322682466305, 646551227626160139, 673008336010084378)
    async def dismiss(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            """Change overwrite to the default permissions for member"""
            overwrite = {
                member: discord.PermissionOverwrite(send_messages=False, embed_links=False)
            }
            await ctx.channel.edit(overwrites=overwrite)
            await ctx.send(f"{member.mention} has been dismissed from the floor.", ephemeral=True)
        else:
            await ctx.send("This command can only be used in a council session channel.")
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))