import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="remove", description="Fjern en bruger fra ticketen")
    @discord.app_commands.describe(bruger="Brugeren du vil fjerne fra ticketen")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
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

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Pacific - Ticket System",
                    description=(
                        f"{interaction.user.mention} har fjerent en brugere fra ticketn\n"
                        f"Hvis du ønsker at tilføje {user.mention} igen kan du bruge \n`/add user:{user.id}`."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                ),
                ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Der opstod en fejl: {str(e)}",
                ephemeral=True
            )