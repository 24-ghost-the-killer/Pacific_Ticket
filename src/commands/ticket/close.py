import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.model.close import TicketCloseModel
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
class Close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="close", description="Close the current ticket")
    async def close(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Settings.get('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return
        
        ticket = Database.get({ 'channel_id': str(interaction.channel.id) })

        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        
        if not ticket['claimed']:
            await interaction.response.send_message(
                "Denne ticket er ikke blevet taget af en fra personalet. Du kan ikke lukke en ticket, der ikke er taget.",
                ephemeral=True
            )
            return
        
        if not ticket['claimed_by'] == interaction.user.id:
            await interaction.response.send_message(
                "Du kan ikke lukke denne ticket, da du ikke er den, der har taget den.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(TicketCloseModel())