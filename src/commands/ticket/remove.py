import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.logging import Logging

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="remove", description="Fjern en bruger fra ticketen")
    @discord.app_commands.describe(bruger="Brugeren du vil fjerne fra ticketen")
    async def remove(self, interaction: discord.Interaction, bruger: discord.Member):
        try:
            await interaction.response.defer()
            access = Permission(interaction.user, Settings.get('support_role')).check()
            if not access:
                await interaction.response.send_message(
                    "Du har ikke tilladelse til at bruge denne kommando.",
                    ephemeral=True
                )
                return
                        
            ticket = Database.get({
                'channel_id': interaction.channel_id
            })
            
            if not ticket:
                await interaction.followup.send(
                    "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return

            if not ticket['open']:
                await interaction.followup.send(
                    "Denne ticket er lukket. Du kan ikke fjerne brugere fra en lukket ticket.",
                    ephemeral=True
                )
                return

            try:
                overwrites = interaction.channel.overwrites
                if bruger in overwrites:
                    del overwrites[bruger]
                    await interaction.channel.edit(overwrites=overwrites)

                await bruger.send(
                    embed=discord.Embed(
                        title="Pacific - Ticket System",
                        description=(
                            f"Du er blevet fjernet fra en ticket på Pacific\n\n"
                            f"**Ticket ID: **`{ticket['id']}`\n"
                            f"**Fjernet af: **{interaction.user.mention}\n\n"
                            f"Har du spørgsmål eller brug for hjælp, så opret en ticket her: <#{Settings.get('ticket_channel')}>."
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
                            f"{interaction.user.mention} har fjerent en brugere fra ticketn\n"
                            f"Hvis du ønsker at tilføje {bruger.mention} igen kan du bruge \n`/add bruger:{bruger.id}`."
                        ),
                        color=discord.Color.blue()
                    ).set_footer(
                        text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                        icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                    ),
                    ephemeral=False
                )

                await Logging().remove(interaction=interaction, data={ 'user': bruger.id, 'ticket': ticket})
            except Exception as e:
                await interaction.followup.send(
                    f"Der opstod en fejl: {str(e)}",
                    ephemeral=True
                )
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.followup.send(
                "Jeg har ikke tilladelse til at fjerne brugeren fra denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.followup.send(
                f"Der opstod en fejl under fjernelse af brugeren: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.followup.send(
                "Der opstod en fejl under fjernelse af brugeren. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return