import discord
import os
import subprocess

from discord import app_commands
from discord.ext import commands

def get_chat_exporter_path():
    if os.name == 'nt': # windows environment
        return f'.{os.sep}DiscordChatExporter.CLI{os.sep}DiscordChatExporter.Cli.exe'
    elif os.name == 'posix': # linux environment
        return f'dotnet .{os.sep}home{os.sep}pi{os.sep}DiscordChatExporter.CLI{os.sep}DiscordChatExporter.Cli.dll'
    else:
        return

class ClerkCog(commands.Cog, name="Clerk Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='transcript', description='Get a transcript of the session')
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_role(763471193524535336))
    #@commands.has_role(763471193524535336)
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

    @commands.command(name='transcript-display')
    @commands.guild_only()
    @commands.is_owner()
    async def transcript_display(self, ctx: commands.Context) -> None:
        channel = ctx.bot.get_channel(1054420793913770025)
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-1-transcript.html", filename=f"council-session-1-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-2-transcript.html", filename=f"council-session-2-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-3-transcript.html", filename=f"council-session-3-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-4-transcript.html", filename=f"council-session-4-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-5-transcript.html", filename=f"council-session-5-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-6-transcript.html", filename=f"council-session-6-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-7-transcript.html", filename=f"council-session-7-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-8-transcript.html", filename=f"council-session-8-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-9-transcript.html", filename=f"council-session-9-transcript.html"))
        await channel.send(file=discord.File("/home/pi/Documents/Room-Sealer/transcripts/council-session-10-transcript.html", filename=f"council-session-10-transcript.html"))
        pass

    @commands.hybrid_command(name='transcript-simple', description='Get a transcript of the session (Simple Version)')
    @commands.guild_only()
    @commands.is_owner()
    #@commands.has_role(763471193524535336)
    async def transcript_colorful(self, ctx: commands.Context) -> None:
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            path = get_chat_exporter_path()
            if not path:
                raise commands.CommandError("Unsupported OS")
            file_path = f"{ctx.channel.name}-transcript.html"
            subprocess.run([path, "export", "-t", "html", "-c", "redwood", "-o", file_path, "-f", "html", "-b", "0", "-e", "0", "-i", str(ctx.channel.id)])
            await ctx.send(file=discord.File(file_path, filename=file_path))
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClerkCog(bot))
