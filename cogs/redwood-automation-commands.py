import discord
import datetime

from discord.ext import commands
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class CommandsCog(commands.Cog, name="Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.guild_only()
    async def ping_command(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Color.green(),
            description=f''':ping_pong: ***Pong!***
**Latency:** {round(self.bot.latency * 1000)}ms'''
            )
        await ctx.send(embed=embed)
        pass

    @commands.hybrid_command(name="source", description="Get the source code of the bot.")
    @commands.guild_only()
    async def source_command(self, ctx: commands.Context):
        await ctx.send("Check out the source code for Redwood Deli and help add to the bot here: https://github.com/LIPDProductionsInc/Redwood_Automation")
        pass

    @commands.hybrid_command(name="serverinfo", description="Get information about the server.")
    @commands.guild_only()
    async def serverinfo_command(self, ctx: commands.Context):
        embed = discord.Embed(
            title=ctx.guild.name,
            colour=discord.Color.dark_blue()
            )
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True).add_field(name="Category Channels", value=len(ctx.guild.categories), inline=True).add_field(name="Text Channels", value=len(ctx.guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels), inline=True).add_field(name="Members", value=ctx.guild.member_count, inline=True).add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Created At", value=ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Developed by {self.bot.owner} | Server ID: {ctx.guild.id}")
        await ctx.send(embed=embed)
        pass

    @commands.hybrid_command(name="userinfo", description="Get information about a user.", aliases=["whois"])
    @commands.guild_only()
    async def userinfo_command(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
            pass
        embed = discord.Embed(
            title=member.name,
            colour=member.colour
            )
        embed.add_field(name="ID", value=member.id, inline=True).add_field(name="Nickname", value=member.nick, inline=True).add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name="Created At", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name="Bot?", value=member.bot, inline=True)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles]), inline=False)
        embed.add_field(name="Key Permissions", value=", ".join([perm[0] for perm in member.guild_permissions if perm[1]]), inline=False)
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        await ctx.send(embed=embed)
        pass

    @commands.hybrid_command(name="avatar", description="Get the avatar of a user.", aliases=["pfp", "av"])
    @commands.guild_only()
    async def avatar_command(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
            pass
        embed = discord.Embed(
            title=f"{member.name}'s Avatar",
            colour=member.colour
            )
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"Developed by {self.bot.owner} | User ID: {member.id}")
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandsCog(bot))