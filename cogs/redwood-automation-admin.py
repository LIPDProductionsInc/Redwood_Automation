import discord
import asyncio
import datetime
import os
import typing

from discord import app_commands
from discord.ext import commands
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

class AdminCog(commands.Cog, name="Admin Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="ban", description="Ban a member")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban", reason="The reason for the ban", save_messages="Whether or not to save messages from the user")
    async def ban_command(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None, save_messages:Literal["True","False"]="True"):
        if member == None and reason == None:
            embed=discord.Embed(
                title='**Command: Ban**',
                type='rich',
                colour=discord.Color.blue(),
                description='''**Aliases:** /ban
**Description:** Ban a member
**Cooldown:** 3 seconds
**Usage:**
!ban <user> <reason>
**Example:**
!ban @FrostEpresso spamming
'''
            )
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            if save_messages == "True":
                await member.ban(reason=reason, delete_message_days=0)
            else:
                await member.ban(reason=reason)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was banned*** | {reason}'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.red()
            #    )
            #embed2.set_author(name=f"Ban | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="city-ban", description="Ban a member from both city Discord servers")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban", reason="The reason for the ban", save_messages="Whether or not to save messages from the user")
    async def city_ban_command(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None, save_messages:Literal["True","False"]="True"):
        if member == None and reason == None:
            embed=discord.Embed(
                title='**Command: City Ban**',
                type='rich',
                colour=discord.Color.blue(),
                description='''**Aliases: /city-ban**
**Description:** Ban a member from both the city Discord and the RPD Discord
**Cooldown:** 3 seconds
**Usage:** !city-ban <user> <reason>
**Example:** !city-ban @FrostEpresso spamming'''
            )
            await ctx.send(embed=embed)
        else:
            redwood_guild = ctx.bot.get_guild(646540220539338773)
            rpd_guild = ctx.bot.get_guild(1005182438265335901)
            if redwood_guild.get_member(ctx.author.id).guild_permissions.ban_members and rpd_guild.get_member(ctx.author.id).guild_permissions.ban_members:
                if save_messages == "True":
                    await member.ban(reason=reason, delete_message_days=0)
                else:
                    await member.ban(reason=reason)
                embed=discord.Embed(
                    colour=discord.Color.green(),
                    description=f''':white_check_mark: ***{member} was banned from the city Discord and the RPD Discord*** | {reason}'''
                    )
                #embed2=discord.Embed(
                #    colour=discord.Color.red()
                #    )
                #embed2.set_author(name=f"Ban | {member}", icon_url=member.avatar_url)
                #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
                #embed2.set_footer(text=f"ID: {member.id}")
                #embed2.timestamp=datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                #await channel.send(embed=embed2)
                pass
            else:
                raise commands.MissingPermissions(["ban_members"])
            pass
        pass

    @commands.hybrid_command(name="kick", description="Kick a member.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick", reason="The reason for kicking the member")
    async def kick_command(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if member == None and reason == None:
            embed=discord.Embed(
                title='**Command: !kick**',
                colour=discord.Color.blue(),
                description='''**Aliases: /kick**
**Description:** Kick a member.
**Cooldown:** 3 seconds
**Usage:** !kick <user> <reason>
**Example:** !kick @FrostEpresso Spamming'''
            )
            await ctx.send(embed=embed)
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            await member.kick(reason=reason)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was kicked*** | {reason}'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.red()
            #    )
            #embed2.set_author(name=f"Kick | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="unban", description="Unban a member")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to unban")
    async def unban_command(self, ctx: commands.Context, *, member: discord.User = None):
        if member == None:
            embed=discord.Embed(
                title='**Command: !unban**',
                colour=discord.Color.blue(),
                description='''**Aliases:** /unban
**Description:** Unban a member
**Cooldown:** 3 seconds
**Usage:** !unban <user>
**Example:** !unban @FrostEpresso'''
            )
            await ctx.send(embed=embed)
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            await ctx.guild.unban(member)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was unbanned***'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.green()
            #    )
            #embed2.set_author(name=f"Unban | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="city-unban", description="Unban a member from both city Discord servers")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to unban")
    async def city_unban_command(self, ctx: commands.Context, *, member: discord.User = None):
        if member == None:
            embed=discord.Embed(
                title='**Command: !city-unban**',
                colour=discord.Color.blue(),
                description='''**Aliases:** /city-unban
**Description:** Unban a member from both city Discord servers
**Cooldown:** 3 seconds
**Usage:** !city-unban <user>
**Example:** !city-unban @FrostEpresso'''
            )
            await ctx.send(embed=embed)
        else:
            redwood_guild = ctx.bot.get_guild(646540220539338773)
            rpd_guild = ctx.bot.get_guild(1005182438265335901)
            if redwood_guild.get_member(ctx.author.id).guild_permissions.ban_members and rpd_guild.get_member(ctx.author.id).guild_permissions.ban_members:
                #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
                await redwood_guild.unban(member)
                await rpd_guild.unban(member)
                embed=discord.Embed(
                    colour=discord.Color.green(),
                    description=f''':white_check_mark: ***{member} was unbanned from both City Discord servers***'''
                    )
                #embed2=discord.Embed(
                #    colour=discord.Color.green()
                #    )
                #embed2.set_author(name=f"City Unban | {member}", icon_url=member.avatar_url)
                #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True)
                #embed2.set_footer(text=f"ID: {member.id}")
                #embed2.timestamp=datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                #await channel.send(embed=embed2)
                pass
            else:
                raise commands.MissingPermissions(["ban_members"])
            pass
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))