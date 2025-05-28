import discord
from discord.ext import commands
from src.utils.ticket.dropdown import TicketDropdown

async def setup(bot):
    persistent_view = discord.ui.View(timeout=None)
    persistent_view.add_item(TicketDropdown())
    bot.add_view(persistent_view)
    await bot.add_cog(Panel(bot))

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="panel", description="Create a new ticket panel")
    async def panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="RadientRP - Ticket System",
            description=(
                "Hej og velkommen til RadientRP's ticket support!\n\n"
                "Vælg venligst en kategori nedenfor for at oprette en ticket.\n"
                "Hvis du har brug for hjælp, kan du kontakte en administrator.\n\n"
                "**Kategorier:**\n"
                "🔧 **Support:** Få hjælp til spørgsmål eller generelle problemer.\n"
                "🔓 **Unban:** Hjælp vedrørende FiveGuard eller TX bans.\n"
                "💰 **Donation:** Spørgsmål om donationer.\n"
                "👥 **Staff:** Kontakt vores staff."
            ),
            color=discord.Color.red(),
        )
        embed.set_footer(
            text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )
        view = discord.ui.View(timeout=None)
        view.add_item(TicketDropdown())
        await interaction.response.send_message(
            embed=embed,
            view=view,
        )