import discord
import asyncio

from discord import app_commands
from discord.ext import commands

class ClerkCog(commands.Cog, name="Clerk Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='transcript', description='Get a transcript of the session')
    @commands.guild_only()
    @commands.has_role(763471193524535336)
    async def transcript(self, ctx: commands.Context) -> None:
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            transcript = ""
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                transcript += f"{message.author.display_name} (ID {message.author.id}): {message.content}<br>"
            with open("transcript.html", "w") as file:
                file.write(transcript)
            await ctx.send(file=discord.File("transcript.html", filename=f"{ctx.channel.name}-transcript.html"))
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
        pass

    @commands.hybrid_command(name='transcript-colorful', description='Get a transcript of the session (Colorful Version)')
    @commands.guild_only()
    @commands.is_owner()
    #@commands.has_role(763471193524535336)
    async def transcript(self, ctx: commands.Context) -> None:
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            transcript = "<!DOCTYPE html>\n<html lang=\"en\">\n<head></head>\n<body>\n"
            transcript += f"<div class=\"session_preamble\">\n<div class=\"session_preamble_guild_icon\>\n<img src=\"{ctx.guild.icon}\" alt=\"Guild Icon\">\n</div>\n"
            transcript += f"<div class=\"session_preamble_entries-container\">\n<div id=\"guild_name\">{ctx.guild.name}</div>\n"
            transcript += f"<div id=\"session_name\">{ctx.channel.name}</div>\n"
            count = 0
            async for message in ctx.channel.history(limit=None):
                count += 1
                transcript += f"<div class=\"total_message_count\">Messages: {count}</div>\n</div>\n</div>\n"
            transcript += "<div id=\"chatlog\" class=\"chatlog\">\n"
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                transcript += "<div class=\"chatlog_message_group\">\n"
                transcript += f"<div class=\"chatlog_author-avatar-container\">\n<img class=\"chatlog_author-avatar\" src=\"{message.author.avatar}\" alt=\"Avatar\">\n</div>\n"
                transcript += f"<div class=\"chatlog_messages\">\n<span class=\"chatlog_author-name\" title=\"{message.author.name}\" data-user-id=\"{message.author.id}\" style=\"color: {message.author.color}\">{message.author.display_name}[{message.author.id}]</span>\n"
                transcript += f"<span class=\"chatlog_timestamp\">{message.created_at}</span>\n"
                transcript += f"<div id=\"message - {message.id}\" class=\"chatlog_message\" data-message-id=\"{message.id}\ title=Message sent: {message.created_at}\">\n"
                transcript += f"<div class=\"chatlog_content\">\n<div class=\"markdown\"><span class=\"preserve-whitespace\">\n{message.content}</span>\n</div>\n</div>\n</div>\n"
                if message.embeds:
                    for embed in message.embeds:
                        transcript += f"<div class=\"chatlog_embed\">\n<div class=\"chatlog_embed-content-container\">\n<div class=\"chatlog_embed-content\">\n"
                        transcript += f"<div class=\"chatlog_embed-text\">\n<div class=\"chatlog_embed-title\">\n"
                        transcript += f"<a class=\"chatlog_embed-title-link\" href=\"{embed.url}\"><div class=\"markdown preserve-whitespace\">{embed.title}\n</div></a>\n"
                        transcript += f"<div class=\"chatlog_embed-description\">\n<div class=\"markdown preserve-whitespace\">{embed.description}\n</div>"
                        transcript += f"</div>\n</div>\n</div>\n</div>\n</div>\n"
                transcript += "</div>\n</div>\n</div>\n"
            transcript += "</div>\n</body>\n</html>"
            with open("transcript.html", "w") as file:
                file.write(transcript)
            await ctx.send(file=discord.File("transcript.html", filename=f"{ctx.channel.name}-transcript.html"))
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClerkCog(bot))