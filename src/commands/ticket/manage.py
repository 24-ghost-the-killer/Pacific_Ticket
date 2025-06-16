import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.database.main import Database as Database
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.dropdown.manager import SettingsDropdown

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="manage", description="Administrer indstillinger for ticket systemet")
    async def manage(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Settings.get('panel_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return
        class SettingsView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(SettingsDropdown())

        embed = discord.Embed(
            title="Manage Ticket",
            description="Vælg en indstilling fra dropdown-menuen nedenfor.",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=SettingsView(), ephemeral=True)