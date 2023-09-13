import discord
import aiosqlite
import typing

from discord.ext import commands
from discord import app_commands
from typing import Literal

class StoretoDBCog(commands.Cog, name="Store to Database Group Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="store", description="Store to Database Group Commands")

    @group.command(name="decree", description="Store a mayoral decree to the database")
    @app_commands.checks.has_any_role(1150770058897920157)
    @app_commands.guild_only()
    @app_commands.describe(decree_name="Name of the decree", decree_number="Number of the decree", signed_by="Who signed the decree?", decree_status="Status of the decree", decree_link="Link to the decree")
    async def decree(self, interaction: discord.Interaction, decree_name:str, decree_number:int, signed_by:str, decree_status:Literal["Active", "Inactive", "Repealed"], decree_link:str):
        if decree_link.startswith("https://drive.google.com/file/d/") or decree_link.startswith("https://forums.stateoffirestone.com/") or decree_link.startswith("https://docs.google.com/document/d/"):
            async with aiosqlite.connect("/home/pi/Documents/Redwood_Automation/db/redwood_backup.db") as db:
                try:
                    await db.execute(f"INSERT INTO decrees values('{decree_name}', {decree_number}, '{decree_status}', '{signed_by}', '{decree_link}')")
                    print(f'Added Mayoral Decree {decree_number} - {decree_name} to database')
                    await db.commit()
                    print('Saved')
                    await interaction.response.send_message(content="Decree stored to database!", ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)
                    print(f'Ignoring exception in command decree: {e}')
                    pass
                pass
        else:
            await interaction.response.send_message("Use a Google Drive or Forums link", ephemeral=True)
            pass
        pass

    @group.command(name="legislation", description="Store legislation to the database")
    @app_commands.checks.has_any_role(1150770058897920157)
    @app_commands.guild_only()
    @app_commands.describe(legislation_name="Name of the legislation", legislation_type="Type of legislation", legislation_status="Status of the legislation", legislation_link="Link to the legislation")
    async def legislation(self, interaction: discord.Interaction, legislation_name:str, legislation_type:Literal["Bill", "Resolution", "Amendment", "Charter Amendment"], legislation_status:Literal["Passed", "Failed", "Vetoed", "Nullified"], legislation_link:str):
        if legislation_link.startswith("https://drive.google.com/file/d/") or legislation_link.startswith("https://forums.stateoffirestone.com/") or legislation_link.startswith("https://docs.google.com/document/d/"):
            async with aiosqlite.connect("/home/pi/Documents/Redwood_Automation/db/redwood_backup.db") as db:
                try:
                    await db.execute(f"INSERT INTO legislation values('{legislation_name}', '{legislation_type}', '{legislation_status}', '{legislation_link}')")
                    print(f'Added {legislation_type} {legislation_name} to database')
                    await db.commit()
                    print('Saved')
                    await interaction.response.send_message(content="Legislation stored to database!", ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)
                    print(f'Ignoring exception in command legislation: {e}')
                    pass
                pass
        else:
            await interaction.response.send_message("Use a Google Drive or Forums link", ephemeral=True)
            pass
        pass

    @group.command(name="employment", description="Store an employment, either by confirmation or nomination, to the database")
    @app_commands.checks.has_any_role(1150770058897920157)
    @app_commands.guild_only()
    @app_commands.describe(employee="The name of the employee", member="The Discord account of the employee", appointment="Were they confirmed or nominated?", status="Did it pass or fail?", position="What position were they employed to?")
    async def employment(self, interaction: discord.Interaction, employee:str, member:discord.Member, appointment:Literal["Confirmation", "Nomination"], status:Literal["Passed", "Failed"], position:str):
        async with aiosqlite.connect("/home/pi/Documents/Redwood_Automation/db/redwood_backup.db") as db:
            if member is not int:
                member = member.id
            try:
                await db.execute(f"INSERT INTO employment values('{employee}', {member}, '{appointment}', '{status}', '{position}')")
                print(f'Added {employee} to database')
                await db.commit()
                print('Saved')
                await interaction.response.send_message(content="Employment stored to database!", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(content=f"Error: {e}", ephemeral=True)
                print(f'Ignoring exception in command employment: {e}')
                pass
            pass
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StoretoDBCog(bot))