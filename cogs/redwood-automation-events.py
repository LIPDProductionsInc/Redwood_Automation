import discord
import datetime

from discord.ext import commands

class EventsCog(commands.Cog, name="Events Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            if type(before.channel) != discord.DMChannel and type(after.channel) != discord.DMChannel:
                if before.channel.name.startswith('council-session'):
                    channel = self.bot.get_channel(1040322534454861904)
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
    async def on_message_delete(self, message):
        if message.channel.name.startswith('council-session'):
            channel = self.bot.get_channel(1040322534454861904)
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

    '''Listen for when a reaction is added to an embed from Redwood Automation in the #ocr-directors channel (1005535705180672081)'''
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 1005535705180672081:
            if payload.member.has_role(940718179402006590):
                guild = self.bot.get_guild(payload.guild_id)
                message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                if message.author.id == 1028806931390943282:
                    embed = message.embeds[0]
                    field = embed.fields[0]
                    id = field.value
                    id = id[2:-1]
                    member = guild.get_member(int(id))
                    if payload.emoji.name == '✅':
                        role = guild.get_role(762321175900454933)
                        await member.add_roles(role)
                        channel = self.bot.get_channel(646550331991523328)
                        await channel.send(f"{member.mention}: Your request has been approved. You now have the Business Representative role.")
                        #DM here
                        pass
                    if payload.emoji.name == '❌':
                        await member.send("Your request has been denied.")
                        pass
                    pass
                pass
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(EventsCog(bot))