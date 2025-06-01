import discord
from src.database.main import Database
from src.utils.ticket.support import TicketModel as Modal

class TicketCall(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._call_support_enabled = None
        self._call_role_set = None

    def _load_settings(self, guild):
        if self._call_support_enabled is None:
            self._call_support_enabled = Database().setting('call_support')
        if self._call_role_set is None:
            self._call_role_set = Database.setting('call_role')
        if self._support_role_id is None:
            try:
                self._support_role_id = int(Database().setting('support_role'))
            except Exception:
                self._support_role_id = None
        if self._support_role_id:
            self._support_role = guild.get_role(self._support_role_id)
        else:
            self._support_role = None

    @discord.ui.button(label="Indkald", style=discord.ButtonStyle.red, emoji="📞", custom_id="ticket_call")
    async def indkald(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._load_settings(interaction.guild)
        if self._call_support_enabled != 'true':
            await interaction.response.send_message(
                "Indkaldelse af support er ikke aktiveret. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        if self._call_role_set is None:
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
                "Du er ikke staff og kan derfor ikke indkalde personen i support.",
                ephemeral=True
            )
            return

        ticket = Database().get({
            'channel_id': str(interaction.channel.id)
        })
        
        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_modal(Modal())