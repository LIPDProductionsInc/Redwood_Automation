import discord
import datetime
import traceback

from discord import app_commands
from discord.ext import commands

class ApprovalPoll(discord.ui.Modal, title="Title (This is a test)"):

    mayormember = discord.guild.get_role(646549322682466305).members[0].mention if len(discord.guild.get_role(646549322682466305).members) > 0 else None
    deputymayormember = discord.guild.get_role(646551227626160139).members[0].mention if len(discord.guild.get_role(646551227626160139).members) > 0 else None
    chiefofstaffmember = discord.guild.get_role(854157399732387850).members[0].mention if len(discord.guild.get_role(854157399732387850).members) > 0 else None
    deputychiefofstaffmember = discord.guild.get_role(940716304233545758).members[0].mention if len(discord.guild.get_role(940716304233545758).members) > 0 else None
    chairpersonmember = discord.guild.get_role(673008336010084378).members[0].mention if len(discord.guild.get_role(673008336010084378).members) > 0 else None

    if mayormember is not None:
        mayor = discord.ui.TextInput(
            label=f"Do you approve of Mayor {mayormember.display_name} based off their decisions, actions, conduct, and overall term thus far?",
            style=discord.TextStyle.short,
            placeholder="Answer Yes or No",
            required=True,
            min_length=2,
            max_length=3
        )
    
    if deputymayormember is not None:
        deputymayor = discord.ui.TextInput(
            label=f"Do you approve of Deputy Mayor {deputymayormember.display_name} based off their decisions, actions, conduct, and overall term thus far?",
            style=discord.TextStyle.short,
            placeholder="Answer Yes or No",
            required=True,
            min_length=2,
            max_length=3
        )

    cityattorney = discord.ui.TextInput(
        label="Do you approve of City Attorney based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    cityattorneyoffice = discord.ui.TextInput(
        label="Do you approve of the City Attorney's Office as a whole?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    ocrdirector = discord.ui.TextInput(
        label="Do you approve of the Office of Commerce Relations Director based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    ocrdeputydirector = discord.ui.TextInput(
        label="Do you approve of the Office of Commerce Relations Deputy Director based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    ocroffice = discord.ui.TextInput(
        label="Do you approve of the Office of Commerce Relations as a whole?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    if chiefofstaffmember is not None:
        chiefofstaff = discord.ui.TextInput(
            label=f"Do you approve of Chief of Staff {chiefofstaffmember.display_name} based off their decisions, actions, conduct, and overall term thus far?",
            style=discord.TextStyle.short,
            placeholder="Answer Yes or No",
            required=True,
            min_length=2,
            max_length=3
        )

    if deputychiefofstaffmember is not None:
        deputychiefofstaff = discord.ui.TextInput(
            label=f"Do you approve of Deputy Chief of Staff {deputychiefofstaffmember.display_name} based off their decisions, actions, conduct, and overall term thus far?",
            style=discord.TextStyle.short,
            placeholder="Answer Yes or No",
            required=True,
            min_length=2,
            max_length=3
        )

    presssecretary = discord.ui.TextInput(
        label="Do you approve of the Press Secretary based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    policechief = discord.ui.TextInput(
        label="Do you approve of the Police Chief based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    policedepartment = discord.ui.TextInput(
        label="Do you approve of the Redwood Police Department as a whole?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    if chairpersonmember is not None:
        chairperson = discord.ui.TextInput(
            label=f"Do you approve of Chairperson {chairpersonmember.display_name} based off their decisions, actions, conduct, and overall term thus far?",
            style=discord.TextStyle.short,
            placeholder="Answer Yes or No",
            required=True,
            min_length=2,
            max_length=3
        )
    
    citycouncil = discord.ui.TextInput(
        label="Do you approve of the City Council as a whole?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    cityclerk = discord.ui.TextInput(
        label="Do you approve of the City Clerk based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    assistantcityclerk = discord.ui.TextInput(
        label="Do you approve of the Assistant City Clerk based off their decisions, actions, conduct, and overall term thus far?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    government = discord.ui.TextInput(
        label="Do you approve of the Redwood City Government as a whole?",
        style=discord.TextStyle.short,
        placeholder="Answer Yes or No",
        required=True,
        min_length=2,
        max_length=3
    )

    feedback = discord.ui.TextInput(
        label="Is there anything else you'd like to bring up or discuss?",
        style=discord.TextStyle.long,
        placeholder="Answer here",
        required=False,
        min_length=0,
        max_length=1000
    )

    notice = discord.ui.TextInput(
        label="Please answer honestly and to the best of your ability. If you do not answer honestly or use this to troll, moderation action will be taken."
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(808055214287618059)
        await interaction.response.send_message(f'Your feedback has been sent!', ephemeral=True)
        embed = discord.Embed(
            title="Approval Poll",
            colour=discord.Color.dark_blue()
        )
        if self.mayormember is not None:
            embed.add_field(name=f"Approve of Mayor {self.mayormember.display_name}", value=f"{self.mayor.value}", inline=False)
        if self.deputymayormember is not None:
            embed.add_field(name=f"Approve of Deputy Mayor {self.deputymayormember.display_name}", value=self.deputymayor.value, inline=False)
        embed.add_field(name="Approve of the City Attorney", value=self.cityattorney.value, inline=False)
        embed.add_field(name="Approve of the City Attorney's Office", value=self.cityattorneyoffice.value, inline=False)
        embed.add_field(name="Approve of the Office of Commerce Relations Director", value=self.ocrdirector.value, inline=False)
        embed.add_field(name="Approve of the Office of Commerce Relations Deputy Director", value=self.ocrdeputydirector.value, inline=False)
        embed.add_field(name="Approve of the Office of Commerce Relations", value=self.ocroffice.value, inline=False)
        if self.chiefofstaffmember is not None:
            embed.add_field(name=f"Approve of Chief of Staff {self.chiefofstaffmember.display_name}", value=self.chiefofstaff.value, inline=False)
        if self.deputychiefofstaffmember is not None:
            embed.add_field(name=f"Approve of Deputy Chief of Staff {self.deputychiefofstaffmember.display_name}", value=self.deputychiefofstaff.value, inline=False)
        embed.add_field(name="Approve of the Press Secretary", value=self.presssecretary.value, inline=False)
        embed.add_field(name="Approve of the Police Chief", value=self.policechief.value, inline=False)
        embed.add_field(name="Approve of the Redwood Police Department", value=self.policedepartment.value, inline=False)
        if self.chairpersonmember is not None:
            embed.add_field(name=f"Approve of Chairperson {self.chairpersonmember.display_name}", value=self.chairperson.value, inline=False)
        embed.add_field(name="Approve of the City Council", value=self.citycouncil.value, inline=False)
        embed.add_field(name="Approve of the City Clerk", value=self.cityclerk.value, inline=False)
        embed.add_field(name="Approve of the Assistant City Clerk", value=self.assistantcityclerk.value, inline=False)
        embed.add_field(name="Approve of the Redwood City Government", value=self.government.value, inline=False)
        if self.feedback.value is not None:
            embed.add_field(name="Feedback", value=self.feedback.value, inline=False)
        embed.set_footer(text=f'City of Redwood | ID: {interaction.user.id}', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

    pass

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='feedback', description='Send feedback to the Mayor')
    @commands.guild_only()
    @commands.is_owner()
    async def feedback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ApprovalPoll())

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))