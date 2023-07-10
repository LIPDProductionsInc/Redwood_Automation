import discord

from discord import app_commands
from discord.ext import commands

class PressCog(commands.Cog, name="Press Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="tweet", description="Repost a tweet")
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_role(763471106618556416))
    @app_commands.describe(tweet_url="The URL of the tweet to repost")
    async def tweet(self, ctx:commands.Context, tweet_url: str) -> None:
        if tweet_url.startswith("https://twitter.com/"):
            channel = self.bot.get_channel(761960138600349707)
            await channel.send(tweet_url)
            await ctx.send("Tweet sent!", ephemeral=True)
        else:
            raise commands.BadArgument("Invalid tweet URL")
        pass
    
    pass

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(PressCog(bot))
