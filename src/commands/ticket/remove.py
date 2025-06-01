import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.database.main import Database as MainDatabase
from src.utils.ticket.database import TicketDatabase as Database

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="remove", description="Remove a user from the ticket")
    @discord.app_commands.describe(user="The user to remove from the ticket")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        access = Permission(interaction.user, MainDatabase.setting('support_role')).check()
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
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        if not ticket['open']:
            await interaction.response.send_message(
                "Denne ticket er lukket. Du kan ikke fjerne brugere fra en lukket ticket.",
                ephemeral=True
            )
            return

        try:
            overwrites = interaction.channel.overwrites
            if user in overwrites:
                del overwrites[user]
                await interaction.channel.edit(overwrites=overwrites)

            await user.send(
                embed=discord.Embed(
                    title="Radient - Ticket System",
                    description=(
                        f"Du er blevet fjernet fra en ticket på Radient\n\n"
                        f"**Ticket ID: **`{ticket['id']}`\n"
                        f"**Fjernet af: **{interaction.user.mention}\n\n"
                        f"Har du spørgsmål eller brug for hjælp, så opret en ticket her: <#{MainDatabase.setting('ticket_channel')}>."
                    ),
                    color=discord.Color.green()
                ).set_footer(
                    text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
                )
            )   

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Radient - Ticket System",
                    description=(
                        f"{interaction.user.mention} har fjerent en brugere fra ticketn\n"
                        f"Hvis du ønsker at tilføje {user.mention} igen kan du bruge \n`/add user:{user.id}`."
                    ),
                    color=discord.Color.red()
                ).set_footer(
                    text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
                ),
                ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Der opstod en fejl: {str(e)}",
                ephemeral=True
            )