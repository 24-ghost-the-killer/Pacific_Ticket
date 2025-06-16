import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import SettingsDatabase as Settings
class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add", description="Tilføj en bruger til ticketen")
    @discord.app_commands.describe(bruger="Brugeren du vil tilføje til ticketen")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()

        access = Permission(interaction.user, Settings.get('support_role')).check()
        if not access:
            await interaction.followup.send(
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
                "Denne ticket er lukket. Du kan ikke tilføje brugere til en lukket ticket.",
                ephemeral=True
            )
            return

        try:
            await interaction.channel.set_permissions(user, read_messages=True, send_messages=True)

            await user.send(
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
                        f"{interaction.user.mention} har tilføjet en brugere til ticketn\n"
                        f"Hvis du ønsker at fjerne {user.mention} igen kan du bruge \n`/remove user:{user.id}`."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                ),
                ephemeral=False
            )
        except Exception as e:
            await interaction.followup.send(
                f"Der opstod en fejl: {str(e)}",
                ephemeral=True
            )