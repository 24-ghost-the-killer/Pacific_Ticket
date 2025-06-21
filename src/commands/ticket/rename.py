import discord
from discord.ext import commands
from src.database.functions.settings import DatabaseSettings as Settings
from src.utils.ticket.database import TicketDatabase as Database
from src.utils.permissions import Permission
from src.utils.ticket.logging import Logging
class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="rename", description="Omdøb ticketens navn til noget andet")
    @discord.app_commands.describe(navn="Det nye navn til ticketen")
    async def rename(self, interaction: discord.Interaction, navn: str):
        try:
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
                await interaction.channel.edit(name=navn)
                Database.update(interaction.channel.id, {
                    'channel_name': navn
                })

                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Pacific - Ticket System",
                        description=(
                            f"Ticketen er blevet omdøbt af {interaction.user.mention} til `{navn}`.\n"
                            "Hvis du har spørgsmål, kontakt venligst en administrator."
                        ),
                        color=discord.Color.blue()
                    ).set_footer(
                        text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                        icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
                    ),
                    ephemeral=False
                )

                await Logging().rename(interaction=interaction, data={ 'name': navn, 'ticket': ticket })

            except discord.Forbidden as e:
                print(f"Forbidden: {e}")
                await interaction.response.send_message(
                    "Jeg har ikke tilladelse til at ændre navnet på denne ticket. Kontakt venligst en administrator.",
                    ephemeral=True
                )
                return
            except discord.HTTPException as e:
                print(f"HTTPException: {e}")
                await interaction.response.send_message(
                    f"Der opstod en fejl under omdøbning af ticketen: {str(e)}",
                    ephemeral=True
                )
                return
            except Exception as e:
                print(f"Exception: {e}")
                await interaction.response.send_message(
                    f"Der opstod en ukendt fejl: {e}",
                    ephemeral=True
                )
                return
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at omdøbe denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.response.send_message(
                f"Der opstod en fejl under omdøbning af ticketen: {str(e)}",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.response.send_message(
                "Der opstod en fejl under omdøbning af ticketen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

