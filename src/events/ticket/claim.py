import discord
from src.utils.ticket.database import TicketDatabase as Database
from src.events.ticket.unclaim import TicketUnclaim as Unclaim
class TicketClaim(discord.ui.View):
    _category_cache = None

    def __init__(self):
        super().__init__(timeout=None)
        if TicketClaim._category_cache is None:
            categories = Database().categorys() or []
            TicketClaim._category_cache = {str(cat['value']): cat for cat in categories}
            TicketClaim._category_cache.update({cat['value']: cat for cat in categories})

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.red, emoji="🎫", custom_id="ticket_claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = Database().get({'channel_id': str(interaction.channel.id)})
        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        category = TicketClaim._category_cache.get(str(ticket['category']))
        if not category:
            await interaction.response.send_message(
                "Kategorien for denne ticket findes ikke. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        role = interaction.guild.get_role(int(category['role_access'])) if category.get('role_access') else None
        owner = interaction.guild.get_member(int(ticket['owner_id'])) if ticket.get('owner_id') else None
        if not role:
            await interaction.response.send_message(
                "Rollen for denne ticket findes ikke. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        if not owner:
            await interaction.response.send_message(
                "Ejeren af denne ticket findes ikke. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        overwrites = interaction.channel.overwrites
        overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(read_messages=False)
        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
        overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        try:
            await interaction.channel.edit(overwrites=overwrites)
        except discord.Forbidden:
            await interaction.response.send_message(
                "Jeg har ikke tilladelse til at ændre tilladelserne for denne ticket. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"Der opstod en fejl under ændring af tilladelserne: {e}",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="**RadientRP - Ticket System**",
            description=(
                f"{interaction.user.mention} har nu claimet denne ticket.\n"
                f"Kun dig og ejeren ({owner.mention}) kan skrive. Supportrollen kan ikke længere skrive."
            ),
            color=discord.Color.red()
        )
        embed.set_footer(
            text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )
        await interaction.response.send_message(embed=embed, view=Unclaim(), ephemeral=False)

        Database().update({
            'channel_id': str(interaction.channel.id),
            'claimed': True,
            'claimed_by': str(interaction.user.id),
        })