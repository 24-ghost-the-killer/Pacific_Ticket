import discord
from src.utils.ticket.model.call import Model
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
class TicketCall(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._call_support_enabled = None
        self._call_role_set = None

    def _load_settings(self, guild):
        if self._call_support_enabled is None:
            self._call_support_enabled = Settings.get('call_support')
        if self._call_role_set is None:
            self._call_role_set = Settings.get('call_role')
        if self._support_role_id is None:
            try:
                self._support_role_id = int(Settings.get('support_role'))
            except Exception:
                self._support_role_id = None
        if self._support_role_id:
            self._support_role = guild.get_role(self._support_role_id)
        else:
            self._support_role = None

    @discord.ui.button(label="Indkald", style=discord.ButtonStyle.red, emoji="📞", custom_id="ticket_call")
    async def indkald(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
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
            
            if not ticket['claimed_by'] == str(interaction.user.id):
                await interaction.response.send_message(
                    "Du kan ikke indkalde ejeren af ticketen til support, da du ikke er den, der har taget ticketen.",
                    ephemeral=True
                )
                return
            
            await interaction.response.send_modal(Model())
        except Exception as e:
            print(f"Exception: {e}")
            if interaction.response.is_done():
                await interaction.followup.send(
                    "Der opstod en fejl under behandlingen af din anmodning. Prøv venligst igen senere.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Der opstod en fejl under behandlingen af din anmodning. Prøv venligst igen senere.",
                    ephemeral=True
                )
            return