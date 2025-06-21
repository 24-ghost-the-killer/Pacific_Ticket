import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.database import TicketDatabase as Database
from src.utils.ticket.logging import Logging
class Unclaim(commands.Cog):
    _category_cache = None
    def __init__(self, bot):
        self.bot = bot
        if Unclaim._category_cache is None:
            categories = Database().categorys() or []
            Unclaim._category_cache = {str(cat['value']): cat for cat in categories}
            Unclaim._category_cache.update({cat['value']: cat for cat in categories})

    @discord.app_commands.command(name="unclaim", description="Unclaim en ticket, så supportrollen kan skrive igen")
    async def claim(self, interaction: discord.Interaction):
        try:
            access = Permission(interaction.user, Settings.get('support_role')).check()
            if not access:
                await interaction.response.send_message(
                    "Du har ikke tilladelse til at bruge denne kommando.",
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

            if not ticket.get('claimed'):
                await interaction.response.send_message(
                    "Denne ticket er ikke blevet claimet endnu.",
                    ephemeral=True
                )
                return

            if not ticket.get('claimed_by') or str(interaction.user.id) != str(ticket['claimed_by']):
                await interaction.response.send_message(
                    "Kun personen der har claimet denne ticket kan bruge denne knap.",
                    ephemeral=True
                )
                return
            
            if ticket['owner_id'] == str(interaction.user.id):
                await interaction.response.send_message(
                    "Du kan ikke unclaim en ticket du selv har oprettet.",
                    ephemeral=True
                )
                return

            category = Unclaim._category_cache.get(str(ticket['category']))
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

            Database.update(interaction.channel.id, {
                'channel_id': str(interaction.channel.id),
                'claimed': False,
                'claimed_by': ''
            })

            await Logging().unclaim(interaction=interaction, data={ 'ticket': ticket })
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at unclaim denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.response.send_message(
                f"Der opstod en fejl under unclaim af ticketen: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.response.send_message(
                "Der opstod en fejl under afvisning af ticketen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return