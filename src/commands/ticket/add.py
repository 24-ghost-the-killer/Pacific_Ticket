import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.logging import Logging
class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add", description="Tilføj en bruger til ticketen")
    @discord.app_commands.describe(bruger="Brugeren du vil tilføje til ticketen")
    async def add(self, interaction: discord.Interaction, bruger: discord.Member):
        try:
            await interaction.response.defer()

            access = Permission(interaction.user, Settings.get('support_role')).check()
            if not access:
                await interaction.followup.send(
                    "Du har ikke tilladelse til at bruge denne kommando.",
                    ephemeral=True
                )
                return
            
            ticket = Database.get({'channel_id': str(interaction.channel.id)})
            if not ticket:
                await interaction.followup.send(
                    "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return

            if not ticket['open']:
                await interaction.followup.send(
                    "Denne ticket er lukket. Du kan ikke tilføje brugere til en lukket ticket.",
                    ephemeral=True
                )
                return

            await interaction.channel.set_permissions(bruger, read_messages=True, send_messages=True)

            await bruger.send(
                embed=discord.Embed(
                    title="Pacific - Ticket System",
                    description=(
                        f"Du er blevet tilføjet til en ticket på Pacific\n"
                        f"Du kan tilgå ticketen her: {interaction.channel.mention}\n\n"
                        f"**Ticket ID: **`{ticket['id']}`\n"
                        f"**Tilføjet af: **{interaction.user.mention}\n"
                        "Har du spørgsmål eller brug for hjælp, så kontakt venligst en administrator."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                )
            )

            await interaction.followup.send(
                embed=discord.Embed(
                    title="Pacific - Ticket System",
                    description=(
                        f"{interaction.user.mention} har tilføjet en bruger til ticketen\n"
                        f"Hvis du ønsker at fjerne {bruger.mention} igen kan du bruge \n`/remove bruger:{bruger.id}`."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                ),
                ephemeral=False
            )

            await Logging().add(interaction=interaction, data={ 'user': bruger.id, 'ticket': ticket})

        except discord.Forbidden as e:
            print(f"Fobidden: {e}")
            await interaction.followup.send(
                "Jeg har ikke tilladelse til at tilføje brugeren til denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.followup.send(
                f"Der opstod en fejl under tilføjelsen af brugeren: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.followup.send(
                "Der opstod en fejl under behandlingen af din anmodning. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return