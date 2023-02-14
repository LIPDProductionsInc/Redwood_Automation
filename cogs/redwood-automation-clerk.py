import discord
import chat_exporter
import io

from discord import app_commands
from discord.ext import commands

class ClerkCog(commands.Cog, name="Clerk Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='transcript', description='Get a transcript of the session')
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_role(763471193524535336))
    #@commands.has_role(763471193524535336)
    async def transcript(self, ctx: commands.Context) -> None:
        channel = ctx.bot.get_channel(1054420793913770025)
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            try:
                transcript = await chat_exporter.export(ctx.channel, tz_info='EST', fancy_times=True)
                transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"{ctx.channel.name}.html")
                await channel.send(f"{ctx.channel.name}", file=transcript_file)
                transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"{ctx.channel.name}.html")
                await ctx.send(file=transcript_file)
            except Exception as e:
                await ctx.send(f"`{e}`", ephemeral=True)
                print("Ignoring exception in command transcript: {}".format(e))
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

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClerkCog(bot))
