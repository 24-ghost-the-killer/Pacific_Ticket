import discord
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.logging import Logging

class Model(discord.ui.Modal, title="Indkald til support"):
    def __init__(self):
        super().__init__(timeout=None)
        self.call_role = Settings.get('call_role')

    reason = discord.ui.TextInput(
        label="Årsag til indkaldelse",
        style=discord.TextStyle.paragraph,
        placeholder="Skriv her din årsag til at indkalde personen...",
        required=True,
        max_length=500,
        custom_id="ticket_reason"
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)  # Extend interaction validity

            ticket = Database.get({
                'channel_id': interaction.channel.id
            })

            if not ticket:
                await interaction.followup.send(
                    "Der opstod en fejl under hentning af data. Prøv venligst igen.",
                    ephemeral=True
                )
                return
            
            owner = interaction.guild.get_member(int(ticket['owner_id']))
            if not owner.id == interaction.user.id:
                embed = discord.Embed(
                    title="**Pacific - Support Indkaldelse**",
                    description=(
                        f"Du er blevet indkaldt til support fra en ticket på Pacific.\n"
                        f"Du kan tilgå din ticket her: {interaction.channel.jump_url}\n\n"
                        f"**Ticket ID:** `{ticket['id']}`\n"
                        f"**Indkaldt af:** {interaction.user.mention}\n"
                        f"> {self.reason.value}"
                    ),
                    color=discord.Color.blue(),
                )
                embed.set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                )

                try:
                    await owner.send(embed=embed)
                except discord.Forbidden:
                    await interaction.followup.send(
                        "Jeg kunne ikke sende en besked til ejeren af ticketen. Sørg for, at de har direkte beskeder aktiveret.",
                        ephemeral=True
                    )
                    return
                except Exception as e:
                    await interaction.followup.send(
                        f"Der opstod en fejl under afsendelse af beskeden: {e}",
                        ephemeral=True
                    )
                    return
                
                call_role_id = self.call_role
                if call_role_id is not None:
                    role = interaction.guild.get_role(int(call_role_id))
                    if role and owner:
                        try:
                            await owner.add_roles(role, reason="Indkaldt til support via ticket system")
                        except Exception as e:
                            await interaction.followup.send(
                                f"Der opstod en fejl under tildeling af rolle: {e}",
                                ephemeral=True
                            )
                            return

                response_embed = discord.Embed(
                    title="Pacific - Support Indkaldelse",
                    description=(
                        f"{owner.mention} er blevet indkaldt til support!\n\n"
                        f"**Indkaldt af:** {interaction.user.mention}\n"
                        f"**Årsag:**\n> {self.reason.value}"
                    ),
                    color=discord.Color.blue(),
                )
                response_embed.set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                )
                await interaction.channel.send(embed=response_embed)
                await interaction.followup.send(
                    "Indkaldelse sendt! Ticket-ejeren har fået besked.",
                    ephemeral=True
                )

                await Logging().call(interaction=interaction, data={ 'reason': self.reason.value, 'ticket': ticket })
            else:
                await interaction.followup.send(
                    "Du kan ikke indkalde dig selv til support.",
                    ephemeral=True
                )
                return
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at sende beskeder til ejeren af denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.response.send_message(
                f"Der opstod en fejl under indkaldelse af support: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.response.send_message(
                "Der opstod en fejl under indkaldelse af support. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return