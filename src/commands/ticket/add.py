import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.main import Database as MainDatabase

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add", description="Add a user to the ticket")
    @discord.app_commands.describe(user="The user to add to the ticket")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()  # Acknowledge the interaction immediately

        access = Permission(interaction.user, MainDatabase.setting('support_role')).check()
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
                    title="Radient - Ticket System",
                    description=(
                        f"Du er blevet tilføjet til en ticket på Radient\n"
                        f"Du kan tilgå ticketen her: {interaction.channel.mention}\n\n"
                        f"**Ticket ID: **`{ticket['id']}`\n"
                        f"**Tilføjet af: **{interaction.user.mention}\n"
                        "Har du spørgsmål eller brug for hjælp, så kontakt venligst en administrator."
                    ),
                    color=discord.Color.green()
                ).set_footer(
                    text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
                )
            )

            await interaction.followup.send(
                embed=discord.Embed(
                    title="Radient - Ticket System",
                    description=(
                        f"{interaction.user.mention} har tilføjet en brugere til ticketn\n"
                        f"Hvis du ønsker at fjerne {user.mention} igen kan du bruge \n`/remove user:{user.id}`."
                    ),
                    color=discord.Color.red()
                ).set_footer(
                    text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
                ),
                ephemeral=False
            )
        except Exception as e:
            await interaction.followup.send(
                f"Der opstod en fejl: {str(e)}",
                ephemeral=True
            )