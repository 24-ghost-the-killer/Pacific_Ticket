import discord
from discord.ext import commands
from src.utils.ticket.dropdown.select import CategorySelect
class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="create", description="Create a new ticket")
    async def create(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="Pacific - Ticket System",
                description=(
                    "Hej og velkommen til Pacific's ticket support!\n\n"
                    "Vælg venligst en kategori nedenfor for at oprette en ticket.\n"
                    "Hvis du har brug for hjælp, kan du kontakte en administrator.\n\n"
                    "**Kategorier:**\n"
                    "🔧 **Support:** Få hjælp til spørgsmål eller generelle problemer.\n"
                    "🔓 **Unban:** Hjælp vedrørende FiveGuard eller TX bans.\n"
                    "💰 **Donation:** Spørgsmål om donationer.\n"
                    "👥 **Staff:** Kontakt vores staff."
                ),
                color=discord.Color.blue(),
            )
            embed.set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )
            view = discord.ui.View(timeout=None)
            view.add_item(CategorySelect())
            await interaction.response.send_message(
                ephemeral=True,
                embed=embed,
                view=view,
            )
        except discord.Forbidden as e:
            print(f"Forbidden: {e}")
            await interaction.response.send_message(
                "I do not have permission to create tickets. Please contact an administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            print(f"HTTPException: {e}")
            await interaction.response.send_message(
                "An error occurred while creating the ticket. Please try again later.",
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Exception: {e}")
            await interaction.response.send_message(
                "An error occurred while creating the ticket. Please try again later.",
                ephemeral=True
            )
            return