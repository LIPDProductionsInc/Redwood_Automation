import discord
import random
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

class RedwoodAutomationFun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot) -> None:
       self.bot = bot
    
    @commands.hybrid_command(name="flip", description="Flips a coin.")
    @commands.guild_only()
    async def flip(self, ctx: commands.Context) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            if random.randint(0, 1) == 0:
                await ctx.send("Heads")
            else:
                await ctx.send("Tails")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="roll", description="Rolls a die.")
    @commands.guild_only()
    @app_commands.describe(sides="The number of sides on the die.")
    async def roll(self, ctx:commands.Context, sides:int=6) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            await ctx.send(f"You rolled a {random.randint(1, sides)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="choose", description="Chooses between multiple options.")
    @commands.guild_only()
    @app_commands.describe(choices="The choices to choose from.")
    async def choose(self, ctx:commands.Context, *, choices:str) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            await ctx.send(f' Chose {random.choice(choices)}')
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="8ball", description="Answers a yes/no question.")
    @commands.guild_only()
    @app_commands.describe(question="The question to ask.")
    async def eightball(self, ctx:commands.Context, *, question:str) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            responses = ["It is certain.",
                         "It is decidedly so.",
                         "Without a doubt.",
                         "Yes - definitely.",
                         "You may rely on it.",
                         "As I see it, yes.",
                         "Most likely.",
                         "Outlook good.",
                         "Yes.",
                         "Signs point to yes.",
                         "Reply hazy, try again.",
                         "Ask again later.",
                         "Better not tell you now.",
                         "Cannot predict now.",
                         "Concentrate and ask again.",
                         "Don't count on it.",
                         "My reply is no.",
                         "My sources say no.",
                         "Outlook not so good.",
                         "Very doubtful."]
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="rps", description="Play rock, paper, scissors.")
    @commands.guild_only()
    @app_commands.describe(choice="Rock, paper, or scissors.")
    async def rps(self, ctx:commands.Context, choice:Literal["rock", "paper", "scissors"]) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            choices = ["rock", "paper", "scissors"]
            if choice.lower() not in choices:
                raise commands.UserInputError("Invalid choice.")
            else:
                await ctx.send(f"You chose {choice.lower()}")
                await ctx.send(f"I chose {random.choice(choices)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="rpsls", description="Play rock, paper, scissors, lizard, spock.")
    @commands.guild_only()
    @app_commands.describe(choice="Rock, paper, scissors, lizard, or spock.")
    async def rpsls(self, ctx:commands.Context, choice:Literal["rock", "paper", "scissors", "lizard", "spock"]) -> None:
        if ctx.channel.category_id in [646540220539338775, 1033514363635642479] or ctx.channel.id == 1032977034361716786:
            choices = ["rock", "paper", "scissors", "lizard", "spock"]
            if choice.lower() not in choices:
                raise commands.UserInputError("Invalid choice.")
            else:
                await ctx.send(f"You chose {choice.lower()}")
                await ctx.send(f"I chose {random.choice(choices)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    pass

async def setup(bot):
    await bot.add_cog(RedwoodAutomationFun(bot))