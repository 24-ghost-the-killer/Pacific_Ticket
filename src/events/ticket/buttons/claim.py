import discord
from src.events.ticket.buttons.unclaim import TicketUnclaim as Unclaim
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
class TicketClaim(discord.ui.View):
    _category_cache = None

    def __init__(self):
        super().__init__(timeout=None)
        self._support_role_id = None
        self._support_role = None
        if TicketClaim._category_cache is None:
            categories = Database.categorys() or []
            TicketClaim._category_cache = {str(cat['value']): cat for cat in categories}
            TicketClaim._category_cache.update({cat['value']: cat for cat in categories})

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

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.red, emoji="🎫", custom_id="ticket_claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
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
                    "Du er ikke staff og kan derfor ikke claim denne ticket.",
                    ephemeral=True
                )
                return
            
            ticket = Database.get({'channel_id': str(interaction.channel.id)})
            if not ticket:
                await interaction.response.send_message(
                    "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return
            
            if not ticket['open']:
                await interaction.response.send_message(
                    "Denne ticket er lukket. Du kan ikke claim en lukket ticket.",
                    ephemeral=True
                )
                return
            
            if ticket['claimed']:
                await interaction.response.send_message(
                    "Denne ticket er allerede claimet af en anden bruger.",
                    ephemeral=True
                )
                return
            
            if ticket['owner_id'] == str(interaction.user.id):
                await interaction.response.send_message(
                    "Der skete en fejl, du kan ikke claim en ticket du selv har oprettet.",
                    ephemeral=True
                )
                return
            
            if ticket['owner_id'] == str(interaction.user.id):
                await interaction.response.send_message(
                    "Du kan ikke claim en ticket du selv har oprettet.",
                    ephemeral=True
                )
                return

            category = TicketClaim._category_cache.get(str(ticket['category']))
            if not category:
                await interaction.response.send_message(
                    "Kategorien for denne ticket findes ikke. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return
            role = interaction.guild.get_role(int(category['role_access'])) if category.get('role_access') else None
            owner = interaction.guild.get_member(int(ticket['owner_id'])) if ticket.get('owner_id') else None
            if not role:
                await interaction.response.send_message(
                    "Rollen for denne ticket findes ikke. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return
            if not owner:
                await interaction.response.send_message(
                    "Ejeren af denne ticket findes ikke. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return

            overwrites = interaction.channel.overwrites
            overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
            overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
            try:
                await interaction.channel.edit(overwrites=overwrites, name=f"claimed-{interaction.user.name}",)
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

            embed = discord.Embed(
                title="**Pacific - Ticket System**",
                description=(
                    f"{interaction.user.mention} har nu claimet denne ticket.\n"
                    f"Kun dig og ejeren ({owner.mention}) kan skrive. Supportrollen kan ikke længere skrive."
                ),
                color=discord.Color.blue()
            )
            embed.set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )

            try:
                await interaction.response.send_message(embed=embed, view=Unclaim(), ephemeral=False)
            except discord.errors.NotFound:
                await interaction.followup.send(embed=embed, view=Unclaim(), ephemeral=False)

            Database.update(interaction.channel.id, {
                'channel_id': str(interaction.channel.id),
                'claimed': True,
                'claimed_by': str(interaction.user.id),
            })

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
        except Exception as e:
            await interaction.response.send_message(
                f"Der opstod en fejl under claim af ticketen: {str(e)}",
                ephemeral=True
            )
            return