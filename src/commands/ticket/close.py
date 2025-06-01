import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.close import TicketCloseModel
from src.database.main import Database
class Close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="close", description="Close the current ticket")
    async def close(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Database.setting('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_modal(TicketCloseModel())