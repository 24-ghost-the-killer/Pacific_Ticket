import discord
from src.database.main import Database
from src.utils.ticket.close import TicketCloseModel

class TicketClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._support_role = None

    def _load_settings(self, guild):
        if self._support_role_id is None:
            try:
                self._support_role_id = int(Database.setting('support_role'))
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
        # Åbn modal for at indsamle lukningsårsag
        await interaction.response.send_modal(TicketCloseModel())







