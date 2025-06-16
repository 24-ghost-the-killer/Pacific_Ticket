import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.database import TicketDatabase as Database
from src.database.functions.settings import DatabaseSettings as Settings

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="owner", description="Ændre ejeren af en ticket")
    @discord.app_commands.describe(user="Den nye ejer af ticketen")
    async def owner(self, interaction: discord.Interaction, user: discord.Member):
        access = Permission(interaction.user, Settings.get('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return

        ticket = Database.get({
            'channel_id': str(interaction.channel.id)
        })

        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        if not ticket['open']:
            await interaction.response.send_message(
                "Denne ticket er lukket. Du kan ikke ændre ejeren af en lukket ticket.",
                ephemeral=True
            )
            return

        if ticket.get('owner_id') == str(user.id):
            await interaction.response.send_message(
                "Denne bruger er allerede ejer af ticketen.",
                ephemeral=True
            )
            return

        # Update the database with the new owner
        Database.update(interaction.channel.id, { 
            'channel_name': interaction.channel.name, 
            'owner_id': str(user.id), 
            'owner_username': user.name,
        })

        overwrites = interaction.channel.overwrites
        old_owner = interaction.guild.get_member(int(ticket['owner_id'])) if ticket.get('owner_id') else None
        overwrites[user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        if old_owner:
            overwrites.pop(old_owner, None)

        await interaction.channel.edit(overwrites=overwrites, name=f"ticket-{user.name}")
        await interaction.response.send_message(
            embed=discord.embeds.Embed(
                title="Pacific - Ticket System",
                description=(
                    f"Ejeren af ticketen er blevet ændret til {user.mention} af {interaction.user.mention}.\n"
                    "Hvis du har spørgsmål, kontakt venligst en administrator."
                ),
                color=discord.Color.blue()
            ).set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            ),
            ephemeral=False
        )

        if not user.id == interaction.client.user.id:
            await user.send(
                embed=discord.Embed(
                    title="Pacific - Ticket System",
                    description=(
                        f"Du er blevet sat som ejer af en ticket på Pacific\n"
                        f"Du kan tilgå ticketen her: {interaction.channel.mention}\n\n"
                        f"**Ticket ID: **`{ticket['id']}`\n"
                        f"**Ændret Af: **{interaction.user.mention}\n\n"
                        "Har du spørgsmål eller brug for hjælp, så kontakt venligst en administrator."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                )
            )