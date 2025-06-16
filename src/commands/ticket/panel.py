import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.utils.ticket.dropdown.select import CategorySelect
from src.database.functions.settings import DatabaseSettings as Settings
class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="panel", description="Opret et nyt ticket panel for at oprette en ticket")
    async def panel(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Settings.get('panel_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return

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
            embed=embed,
            view=view,
        )