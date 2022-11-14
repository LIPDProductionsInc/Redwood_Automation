import discord
import datetime
import traceback

from discord import app_commands
from discord.ext import commands

class PollOptions(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Yes", value="Yes"),
            discord.SelectOption(label="No", value="No")
        ]

        super().__init__(placeholder="Select an option", min_values=1, max_values=1, options=options)

class ApprovalPoll(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(PollOptions())

    async def callback(self, interaction: discord.Interaction):
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

    pass

class MayorCog(commands.Cog, name="Mayor Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='feedback', description='Send feedback to the Mayor')
    @commands.guild_only()
    @commands.is_owner()
    async def feedback(self, interaction: discord.Interaction) -> None:
        questionnumber = 0
        mayormember = interaction.Guild.get_role(role_id=646549322682466305).members[0].mention if len(interaction.Guild.get_role(role_id=646549322682466305).members) > 0 else None
        deputymayormember = interaction.Guild.get_role(role_id=646551227626160139).members[0].mention if len(interaction.Guild.get_role(role_id=646551227626160139).members) > 0 else None
        chiefofstaffmember = interaction.Guild.get_role(role_id=854157399732387850).members[0].mention if len(interaction.Guild.get_role(role_id=854157399732387850).members) > 0 else None
        deputychiefofstaffmember = interaction.Guild.get_role(role_id=940716304233545758).members[0].mention if len(interaction.Guild.get_role(role_id=940716304233545758).members) > 0 else None
        chairpersonmember = interaction.Guild.get_role(role_id=673008336010084378).members[0].mention if len(interaction.Guild.get_role(role_id=673008336010084378).members) > 0 else None
        view = ApprovalPoll()
        if mayormember is not None:
            questionnumber += 1
            await interaction.response.send(f"Question {questionnumber}: Do you approve of Mayor {mayormember.display_name} based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
            view.wait()
        if deputymayormember is not None:
            questionnumber += 1
            await interaction.response.send(f"Question {questionnumber}: Do you approve of Deputy Mayor {deputymayormember.display_name} based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
            view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the City Attorney based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the City Attorney's Office as a whole?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Office of Commerce Relations Director based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Office of Commerce Relations Deputy Director based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Office of Commerce Relations as a whole?", ephemeral=True, view=view)
        view.wait()
        if chiefofstaffmember is not None:
            questionnumber += 1
            await interaction.response.send(f"Question {questionnumber}: Do you approve of Chief of Staff {chiefofstaffmember.display_name} based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
            view.wait()
        if deputychiefofstaffmember is not None:
            questionnumber += 1
            await interaction.response.send(f"Question {questionnumber}: Do you approve of Deputy Chief of Staff {deputychiefofstaffmember.display_name} based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
            view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Press Secretary based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Police Chief based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Redwood Police Department as a whole?", ephemeral=True, view=view)
        view.wait()
        if chairpersonmember is not None:
            questionnumber += 1
            await interaction.response.send(f"Question {questionnumber}: Do you approve of Chairperson {chairpersonmember.display_name} based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
            view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the City Council as a whole?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the City Clerk based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Assistant City Clerk based off their decisions, actions, conduct, and overall term thus far?", ephemeral=True, view=view)
        view.wait()
        questionnumber += 1
        await interaction.response.send(f"Question {questionnumber}: Do you approve of the Redwood City Government as a whole?", ephemeral=True, view=view)
        view.wait()
        await interaction.response.send(f"Thank you for your feedback! Your responses have been recorded and will be reviewed by the Mayor.", ephemeral=True)
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MayorCog(bot))