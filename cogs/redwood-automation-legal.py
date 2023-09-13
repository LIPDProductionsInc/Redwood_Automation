import discord
import datetime
import sys
import traceback

from discord.ext import commands
from discord import app_commands

class ComplaintModal(discord.ui.Modal, title="Complaint Form"):
    offender = discord.ui.TextInput(
        label="Who is your complaint against?",
        style=discord.TextStyle.short,
        placeholder="Enter their ROBLOX username and ID here...",
        required=True,
        min_length=3,
        max_length=100
    )

    department = discord.ui.TextInput(
        label="What department/office is the person in?",
        style=discord.TextStyle.short,
        placeholder="Enter the department/office here...",
        required=True,
        min_length=3,
        max_length=60
    )

    date = discord.ui.TextInput(
        label="What date did the incident occur?",
        style=discord.TextStyle.short,
        placeholder="Enter the date here...",
        required=True,
        min_length=6,
        max_length=100
    )

    complaint = discord.ui.TextInput(
        label="What is your complaint?",
        style=discord.TextStyle.long,
        placeholder="Enter your complaint here...",
        required=True,
        min_length=10,
        max_length=1000
    )

    additional = discord.ui.TextInput(
        label="List any evidence and/or witnesses here",
        style=discord.TextStyle.long,
        placeholder="Enter any evidence and/or witnesses here...",
        required=True,
        min_length=0
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Thank you for your complaint! It has been sent for review. It can be seen by the Mayor, Deputy Mayor, RW Chief of Staff, City Attorneys Office, District Attorney, County Executive, and the Founder.", ephemeral=True)
        channel = interaction.client.get_channel(1034315223856840735)
        embed = discord.Embed(
            title="New Complaint",
            description=f"**Offender:**\n{self.offender.value}\n\n**Department/Office:**\n{self.department.value}\n\n**Date:**\n{self.date.value}\n\n**Complaint:**\n{self.complaint.value}\n\n**Evidence/Witnesses:**\n{self.additional.value}\n\n**Submitter:**\n{interaction.user.mention}",
            colour=discord.Color.dark_blue()
        )
        embed.set_footer(text=f"ID: {interaction.user.id}")
        embed.set_thumbnail(url=interaction.guild.me.avatar)
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        await interaction.response.send_message("An error occurred while processing your complaint. Please try again later.", ephemeral=True)
        print('Ignoring exception in modal FeedbackModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        pass

    pass

class RecommendationModal(discord.ui.Modal, title="Recommendation Form"):
    # Trello link to the card
    leg_link = discord.ui.TextInput(
        label="Link to legislation trello card",
        style=discord.TextStyle.short,
        placeholder="https://trello.com/c/cardId",
        required=True,
        max_length=30
    )

    # Review status (a basic boolean check)
    leg_review = discord.ui.TextInput(
        label="Legislation Review Status",
        style=discord.TextStyle.short,
        placeholder="Pass/Fail (or other status)",
        required=True,
        max_length=20
    )

    # Recommendation longform text
    leg_recommendation = discord.ui.TextInput(
        label="Recommendations",
        style=discord.TextStyle.long,
        placeholder="Legislation Recommendations",
        required=False,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        submission_channel = 0

        # Some variables for later
        legislation_link = self.leg_link.value.strip()
        legislation_review = self.leg_review.value.strip()
        legislation_recommendation = self.leg_recommendation.value

        # Defer response until after validation
        await interaction.response.defer(ephemeral=True)

        # Validate fields
        if "?" in legislation_link:
            # Strip out trackers or any other nonsense Atlassian should elect to implement such in the future. Remove this should it be required
            legislation_link = legislation_link[:legislation_link.index("?")]

        # Ensure link to legislation is a trello link
        if legislation_link.startswith(("https://trello.com/c/", "https://www.trello.com/c/", "www.trello.com/c/", "trello.com/c/")) == False:
            raise commands.UserInputError(message="Invalid trello link input - ensure it begins with https://trello.com/c/")

        else:
            if legislation_link.startswith("https://") == False:
                legislation_link = "https://" + legislation_link

        # Check if bot should DM user or post it to channel instead
        await interaction.followup.send("Press \"Confirm\" when finished", view=RecommendationConfirmView((legislation_link, legislation_review, legislation_recommendation)), ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        # Handle for input errors
        if type(error) == commands.UserInputError:
            await interaction.followup.send(f"User input error occured. Please correct the following: `{error}`", ephemeral=True)
        else:
            await interaction.followup.send("An error occurred while processing.", ephemeral=True)

        print('Ignoring exception in modal RecommendationModal:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

class RecommendationConfirmView(discord.ui.View):
    def __init__(self, text_inputs: tuple) -> None:
        super().__init__()

        self.link = text_inputs[0]
        self.status = text_inputs[1]
        self.recommendation = text_inputs[2]

        self.destination_channels = []

    @discord.ui.select(
        custom_id="destination_select",
        options=[
            discord.SelectOption(label="Send to Council", value="default", description="Send to Council text channels and the legal office text chat"),
            discord.SelectOption(label="Send to legal office only", value="legal", description="Only send to the legal office text channel")
        ],
        placeholder="Destination"
    )
    async def select_channels(self, interaction: discord.Interaction, select: discord.ui.Select) -> None:
        council_channels = [646552474265845780]
        legal_channels = [873744876079026218]

        if select.values[0] == "default":
            self.destination_channels = council_channels + legal_channels

        else:
            self.destination_channels = legal_channels

        for child in select.view.children:
            if child.custom_id == "confirm_button":
                child.disabled = False

        brief_channels = "\n\nSend to: "
        brief_channels += " ".join([f"<#{channel_id}>" for channel_id in self.destination_channels])

        await interaction.response.edit_message(content="Press \"Confirm\" when finished" + brief_channels, view=select.view)

    @discord.ui.button(
        custom_id="confirm_button",
        style=discord.ButtonStyle.primary,
        label="Confirm",
        disabled=True
    )
    async def confirmation_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.destination_channels == []:
            await interaction.response.send_message(content="Select a destination!", ephemeral=True)

        else:
            self.clear_items()

            channels_failed = []
            # Get and then send the embed to the channels
            for channel_id in self.destination_channels:
                channel = interaction.client.get_channel(channel_id)

                if channel == None:
                    channels_failed.append((channel_id, "None found with ID"))

                elif type(channel) != discord.TextChannel:
                    channels_failed.append((channel_id, f"Expected TextChannel, not {type(channel)}"))
                
                else:
                    recommendations_embed = discord.Embed(
                        color=discord.Color.dark_blue(),
                        title="Legislation Review",
                        url=self.link,
                        description=f"Status: **{self.status}**\nResponsible:{interaction.user.mention}"
                    )
                    recommendations_embed.set_footer(text=f"ID: {interaction.user.id}")
                    recommendations_embed.set_thumbnail(url=interaction.guild.me.avatar)
                    recommendations_embed.timestamp = datetime.datetime.now()

                    if self.recommendation != "" and type(self.recommendation) != None:
                        recommendations_embed.description += f"\n\nLegal office recommendation(s):\n```{self.recommendation}```"

                    try:
                        await channel.send(content=self.link, embed = recommendations_embed)

                    except discord.HTTPException as err:
                        channels_failed.append((channel_id, f"HTTP Error {err.status}"))
                        print(f'HTTPException in RecommendationConfirmView.confirmation_button: {err.status} (error code: {err.code}): {err.text}')

                    except (ValueError, TypeError) as err:
                        channels_failed.append((channel_id, f"Internal Error: {type(err)}"))
                        print(f"Exception {type(err)} in RecommendationConfirmView.confirmation_button: {err}")

            # Edit the response message with results
            results = ""

            if len(channels_failed) != 0: 
                results += "Error sending recommendations to channel(s):"
                
                for channel_err in channels_failed:
                    channel_id, err = channel_err[0], channel_err[1]
                    results += f"\n<#{channel_id}>: {err}"

            await interaction.response.edit_message(content=f"Submitted\n\n{results}", view=self)
            self.stop()

    @discord.ui.button(
        custom_id="cancel_button", 
        style=discord.ButtonStyle.red,
        label="Cancel"
    )
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(content="Cancelled", view=self)
        self.stop()

class LegalOfficeCog(commands.Cog, name="City Attorney Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="legal-office", description="View the current members of the City Attorney's Office.")
    async def legal_office(self, ctx: commands.Context) -> None:
        city_attorney = 646549330479546379
        admin = 763470466269577216
        moderator = 646554162405834762
        embed = discord.Embed(
            title="Redwood City Attorney's Office",
            description="The current members of the City Attorney's Office are as follows:",
            colour=discord.Color.dark_blue()
        )
        guild = ctx.bot.get_guild(646540220539338773)
        embed.add_field(name="City Attorney", value=[member.mention for member in guild.members if discord.utils.get(member.roles, id=city_attorney) and discord.utils.get(member.roles, id=admin)][0], inline=True)
        if len(discord.utils.get(guild.roles, id=city_attorney).members) == 2:
            embed.add_field(name="Assistant City Attorney", value=[member.mention for member in guild.members if discord.utils.get(member.roles, id=city_attorney) and not discord.utils.get(member.roles, id=admin)][0], inline=False)
        else:
            embed.add_field(name="Assistant City Attorneys", value="\n".join([member.mention for member in guild.members if discord.utils.get(member.roles, id=city_attorney) and not discord.utils.get(member.roles, id=admin)]), inline=False)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.set_footer(text=f"Redwood Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)

    @app_commands.command(name="complaint", description="Submit a complaint against a member of the Redwood City Government.")
    @app_commands.guild_only()
    async def complaint(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ComplaintModal())
        pass

    @app_commands.command(name="recommend-changes", description="Recommend changes to a piece of legislation to the Council")
    @app_commands.guild_only()
    @app_commands.guilds(1150770058847588492)
    @app_commands.checks.has_role(646549330479546379)
    async def recommend_changes(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(RecommendationModal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LegalOfficeCog(bot))