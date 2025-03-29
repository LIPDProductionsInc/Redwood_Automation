import discord
import datetime

from discord.ext import commands

class EventsCog(commands.Cog, name="Events Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after) -> None:
        if before.content != after.content:
            if type(before.channel) != discord.DMChannel and type(after.channel) != discord.DMChannel:
                if before.channel.name.startswith('council-session') and not before.channel.name == 'council-session-test' or 'oath' in before.channel.name:
                    channel = self.bot.get_channel(1154236098525012008) # PO Logs
                    link = "https://discordapp.com/channels/{}/{}/{}".format(before.guild.id, before.channel.id, before.id)
                    embed = discord.Embed(
                        colour = discord.Color.blue(),
                        description = f'**Message edited in** {before.channel.mention} [Jump to Message]({link})'
                        )
                    embed.add_field(name='Before:', value=f'{before.content}', inline=False)
                    embed.add_field(name='After:', value=f'{after.content}', inline=False)
                    embed.set_author(name=f'{before.author}', icon_url=before.author.avatar)
                    embed.set_footer(text=f'ID: {before.author.id}')
                    embed.timestamp = datetime.datetime.now()
                    await channel.send(embed=embed)
                    pass
                if after.content.startswith('[Original Message Deleted]'):
                    await after.delete()
                    pass
                pass
            pass
        pass

    @commands.Cog.listener()
    async def on_message_delete(self, message) -> None:
        if message.channel.name.startswith('council-session') and not message.channel.name == 'council-session-test' or 'oath' in message.channel.name:
            channel = self.bot.get_channel(1154236098525012008) # PO Logs
            link = "https://discordapp.com/channels/{}/{}/{}".format(message.guild.id, message.channel.id, message.id)
            embed = discord.Embed(
                colour = discord.Color.red(),
                description = f'**Message deleted in** {message.channel.mention} [Jump to Message]({link})'
                )
            embed.add_field(name='Message:', value=f'{message.content}', inline=False)
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if entry.target == message.author:
                    embed.add_field(name='Deleted By:', value=f'{entry.user.mention}', inline=False)
                    embed.add_field(name='ID:', value=f'{entry.user.id}', inline=True)
                    break
            embed.set_author(name=f'{message.author}', icon_url=message.author.avatar)
            embed.set_footer(text=f'ID: {message.author.id}')
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
            pass
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        if payload.channel_id == 1150770060684705816: # OCR Director's Channel
            for role in payload.member.roles:
                if role.id == 1150770058935681154:
                    guild = self.bot.get_guild(payload.guild_id)
                    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    if message.author.id == 1028806931390943282: # The Bot
                        channel = self.bot.get_channel(1150770060684705816) # OCR Director's Channel
                        embed = message.embeds[0]
                        field = embed.fields[0]
                        id = field.value
                        id = id[2:-1]
                        member = guild.get_member(int(id))
                        member_role = discord.utils.get(guild.roles, id=1150770058868568108) # Business Representative
                        if member_role in member.roles:
                            await message.remove_reaction(payload.emoji, payload.member)
                            await channel.send(f"{payload.member.mention}: {member.mention} already has the Business Representative role.")
                        else:
                            if payload.emoji.name == '✅':
                                role = guild.get_role(1150770058868568108) # Business Representative
                                await member.add_roles(role)
                                await channel.send(f"Business Representative role has been given to {member.mention}.")
                                await member.send("""**REDWOOD OFFICE OF COMMERCE RELATIONS**\n*CITY OF REDWOOD*\n\nYou have requested the \"Business Representative\" role in the city of Redwood Discord. This role will gain you access to Business announcements and communications channels specifically for Redwood Businesses, in addition to the support of Commerce Relations. 

To better track economic activity, we encourage ALL businesses to register with the City Of Redwood, which gains the Business additional perks such as being able to post in the Business Advertisements channel. You can find more information in the Business Announcements channel as well as view the attached resources: 

https://docs.google.com/forms/d/1DI9AvTgvlr8pgijRtM7fwvWYNt3eopFcK_2rVUvVX8s/edit
https://docs.google.com/document/d/1Fd8uEPCGp7Zhs8N54tgd_Mfb2I4Zy2amIBWefHlEQf8/edit?usp=sharing

If you have any questions or concerns feel free to reach out to an OCR Representative!\n\nThank you""")
                                log = self.bot.get_channel(1150770063411003424) # Log Channel
                                logembed = discord.Embed(
                                    colour = discord.Color.blue(),
                                    description = f'**{member.mention} **was given the** `{role.name}` **role**'
                                    )
                                logembed.set_author(name=f'{member}', icon_url=member.display_avatar)
                                logembed.set_footer(text=f'ID: {member.id}')
                                logembed.timestamp = datetime.datetime.now()
                                await log.send(embed=logembed)
                                pass
                            elif payload.emoji.name == '❌':
                                await member.send("Your request has been denied.")
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if before.guild.id == 1150770058935681154: #Redwood Discord
            # Check if the user was timed out
            if before.timed_out != after.timed_out and after.timed_out is not None:
                channel = self.bot.get_channel(1150770063411003424) # Log Channel
                embed = discord.Embed(
                    colour = discord.Color.red(),
                    description = f'**{after.mention}** was timed out'
                    )
                # Fetch the audit log to find out who issued the timeout
                async for entry in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.member_update):
                    if entry.target.id == after.id and entry.after.timed_out_until:
                        moderator = entry.user
                        duration = (entry.after.timed_out_until - datetime.datetime.now()).total_seconds()
                        reason = entry.reason if entry.reason else "No reason provided"
                        # Add the fields
                        embed.add_field(name='Moderator:', value=f'{moderator.mention}', inline=False)
                        embed.add_field(name='Duration:', value=f'{duration} seconds', inline=False)
                        embed.add_field(name='Reason:', value=reason, inline=False)
                    break # Exit loop once found
                embed.set_author(name=f'{after}', icon_url=after.display_avatar)
                embed.set_footer(text=f'ID: {after.id}')
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=after.display_avatar)
                await channel.send(embed=embed)
                pass
            pass
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventsCog(bot))
