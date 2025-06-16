import discord
from discord.ext import commands
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.database import TicketDatabase as Database
from src.utils.permissions import Permission

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="rename", description="Omdøb ticketens navn til noget andet")
    @discord.app_commands.describe(navn="Det nye navn til ticketen")
    async def rename(self, interaction: discord.Interaction, string: str):
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
        
        try: 
            await interaction.channel.edit(name=string)
            Database.update(interaction.channel.id, {
                'channel_name': string
            })

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Pacific - Ticket System",
                    description=(
                        f"Ticketen er blevet omdøbt af {interaction.user.mention} til `{string}`.\n"
                        "Hvis du har spørgsmål, kontakt venligst en administrator."
                    ),
                    color=discord.Color.blue()
                ).set_footer(
                    text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                    icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
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


