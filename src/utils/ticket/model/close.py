import discord
import datetime
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.logging import Logging
class Model(discord.ui.Modal, title="Lukning af Ticket"):
    reason = discord.ui.TextInput(
        label="Årsag til lukning",
        style=discord.TextStyle.short,
        placeholder="Skriv her din årsag til at lukke ticketen...",
        required=True,
        max_length=50,
        custom_id="ticket_close_reason"
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            ticket = Database.get({
                'channel_id': interaction.channel.id
            })
            
            owner = interaction.guild.get_member(int(ticket['owner_id']))
            if not owner or not isinstance(owner, discord.Member):
                await interaction.response.send_message(
                    "Ejeren af ticketen blev ikke fundet eller er ugyldig. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return
            
            if not ticket['open']:
                await interaction.response.send_message(
                    "Denne ticket er allerede lukket.",
                    ephemeral=True
                )
                return
            
            category = Database.category({ 'value': ticket['category'] })
            role = interaction.guild.get_role(int(category['role_access'])) if category and category.get('role_access') else None
            
            overwrites = interaction.channel.overwrites
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
            overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=False)

            await interaction.channel.edit(overwrites=overwrites, reason=f"Ticket lukket af {interaction.user} ({interaction.user.id})")

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Pacific - Ticket Lukket",
                    description=(
                        f"Din ticket på pacific er ved at blive lukket.\n"
                        f"Du kan ikke længere sende beskeder i denne ticket.\n\n"
                        f"**Ticket ID:** `{ticket['id']}`\n"
                        f"**Lukket af:** {interaction.user.mention}\n"
                        f"> {self.reason.value}"
                    ),
                    color=discord.Color.blue(),
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                )
            )

            Database.update(interaction.channel.id, {
                'open': False,
            })
            
            close_time = int(Settings.get('close_time'))
            await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(seconds=close_time))
            await interaction.channel.delete(reason=f"Ticket lukket af {interaction.user} ({interaction.user.id})")

            embed = discord.Embed(
                title="**Pacific - Ticket Lukket**",
                description=(
                    f"Ticketen er blevet lukket.\n"
                    f"Du kan ikke længere sende beskeder i denne ticket.\n\n"
                    f"**Ticket ID:** `{ticket['id']}`\n"
                    f"**Lukket af:** {interaction.user.mention}\n"
                    f"> {self.reason.value}"
                ),
                color=discord.Color.blue(),
            )
            embed.set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )
                
            await Logging().close(interaction=interaction, data={ 'close_reason': self.reason.value, 'ticket': ticket})

            try:
                await owner.send(embed=embed)
            except discord.Forbidden as e:
                print(f"Forbidden: {e}")
                await interaction.followup.send(
                    "Jeg kunne ikke sende en besked til ejeren af ticketen. Sørg for, at de har direkte beskeder aktiveret.",
                    ephemeral=True
                )
                return
            except discord.HTTPException as e:
                print(f"HTTPException: {e}")
                await interaction.followup.send(
                    f"Der opstod en fejl under afsendelse af beskeden: {str(e)}",
                    ephemeral=True
                )
                return
            except Exception as e:
                print(f"Exception: {e}")
                await interaction.followup.send(
                    f"Der opstod en fejl under afsendelse af beskeden: {e}",
                    ephemeral=True
                )
                return
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at lukke denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.response.send_message(
                f"Der opstod en fejl under lukning af ticketen: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.response.send_message(
                "Der opstod en fejl under lukning af ticketen. Prøv venligst igen.",
                ephemeral=True
            )
            return