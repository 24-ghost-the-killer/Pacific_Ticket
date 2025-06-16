import discord
from src.utils.ticket.close import TicketCloseModel
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
class TicketClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._support_role = None

    def _load_settings(self, guild):
        if self._support_role_id is None:
            try:
                self._support_role_id = int(Settings.get('support_role'))
            except Exception:
                self._support_role_id = None
        if self._support_role_id:
            self._support_role = guild.get_role(self._support_role_id)
        else:
            self._support_role = None

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="ticket_close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._load_settings(interaction.guild)
        if self._support_role_id is None:
            await interaction.response.send_message(
                "Der er ikke angivet en supportrolle. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        if not self._support_role:
            await interaction.response.send_message(
                "Supportrollen blev ikke fundet. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        if self._support_role not in interaction.user.roles:
            await interaction.response.send_message(
                "Du er ikke staff og kan derfor ikke lukke denne ticket.",
                ephemeral=True
            )
            return

        ticket = Database.get({
            'channel_id': str(interaction.channel.id)
        })

        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
    
        await interaction.response.send_modal(TicketCloseModel())







