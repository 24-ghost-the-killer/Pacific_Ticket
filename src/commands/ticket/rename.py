import discord
from discord.ext import commands
from src.database.main import Database as MainDatabase
from src.utils.ticket.database import TicketDatabase as Database
from src.utils.permissions import Permission

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="rename", description="Rename the current ticket")
    @discord.app_commands.describe(string="The new name for the ticket")
    async def rename(self, interaction: discord.Interaction, string: str):
        access = Permission(interaction.user, MainDatabase.setting('support_role')).check()
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
        
        try: 
            await interaction.channel.edit(name=string)

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Radient - Ticket System",
                    description=(
                        f"Ticketen er blevet omdøbt af {interaction.user.mention} til `{string}`.\n"
                        "Hvis du har spørgsmål, kontakt venligst en administrator."
                    ),
                    color=discord.Color.red()
                ).set_footer(
                    text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
                ),
                ephemeral=False
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at ændre navnet på denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Der opstod en ukendt fejl: {e}",
                ephemeral=True
            )


