import discord
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings

class TicketUnclaim(discord.ui.View):
    _category_cache = None

    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._support_role = None
        if TicketUnclaim._category_cache is None:
            categories = Database().categorys() or []
            TicketUnclaim._category_cache = {str(cat['value']): cat for cat in categories}
            TicketUnclaim._category_cache.update({cat['value']: cat for cat in categories})

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
            
    @discord.ui.button(label="Unclaim", style=discord.ButtonStyle.red, emoji="🎫", custom_id="ticket_unclaim")
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
                "Du er ikke staff og kan derfor ikke unclaim denne ticket.",
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

        if not ticket['claimed']:
            await interaction.response.send_message(
                "Denne ticket er ikke blevet claimet endnu.",
                ephemeral=True
            )
            return

        if not ticket['claimed_by'] or str(interaction.user.id) != str(ticket['claimed_by']):
            await interaction.response.send_message(
                "Kun personen der har claimet denne ticket kan bruge denne knap.",
                ephemeral=True
            )
            return
        
        if str(interaction.user.id) == str(ticket['owner_id']):
            await interaction.response.send_message(
                "Du kan ikke unclaim en ticket du selv har oprettet.",
                ephemeral=True
            )
            return

        category = TicketUnclaim._category_cache.get(str(ticket['category']))
        role = interaction.guild.get_role(int(category['role_access'])) if category and category.get('role_access') else None
        owner = interaction.guild.get_member(int(ticket['owner_id'])) if ticket.get('owner_id') else None

        if not category or not role or not owner:
            await interaction.response.send_message(
                "Der opstod en fejl under hentning af kategori, rolle eller ejer. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        overwrites = interaction.channel.overwrites
        if interaction.user in overwrites:
            del overwrites[interaction.user]

        overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        try:
            await interaction.channel.edit(overwrites=overwrites, name=f"ticket-{owner.name}")
        except discord.Forbidden:
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at ændre tilladelserne for denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"Der opstod en fejl under ændring af tilladelserne: {e}",
                ephemeral=True
            )
            return

        Database.update(interaction.channel.id, {
            'channel_id': str(interaction.channel.id),
            'claimed': False,
            'claimed_by': ''
        })

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Ticket Unclaimed",
                description=(
                    f"{interaction.user.mention} har nu unclaimet denne ticket.\n"
                    f"Supportrollen kan nu skrive igen. Ejeren ({owner.mention}) har stadig adgang."
                ),
                color=discord.Color.blue()
            ).set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            ),
            ephemeral=False
        )