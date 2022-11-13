import discord

from discord import app_commands
from discord.ext import commands

class ClerkCog(commands.Cog, name="Clerk Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='transcript', description='Get a transcript of the session')
    @commands.guild_only()
    @commands.is_owner()
    #@commands.has_role(763471193524535336)
    async def transcript(self, ctx: commands.Context) -> None:
        '''Create an HTML transcript of the session, then send the file to the channel'''
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            history = await ctx.channel.history(limit=None).flatten()
            transcript = ""
            for message in history:
                transcript += f"{message.author.display_name}: {message.content}\n"
            with open("transcript.html", "w") as file:
                file.write(transcript)
            await ctx.send(file=discord.File("transcript.html", filename=f"{ctx.channel.name}-transcript.html"))
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClerkCog(bot))