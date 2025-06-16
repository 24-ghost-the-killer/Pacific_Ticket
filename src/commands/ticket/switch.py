import discord
from discord.ext import commands
from src.utils.ticket.database import TicketDatabase as Database
from src.database.main import Database as Settings
from src.utils.permissions import Permission

# Initialize category cache globally
_category_cache = None
if _category_cache is None:
    categories = Database().categorys() or []
    _category_cache = {str(cat['value']): {
        'name': f"{cat['emote']} {cat['label']}",
        'value': cat['value'],
        'channel_category': cat['channel_category'],
        'role_access': cat.get('role_access', None)
    } for cat in categories}

class Switch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="switch", description="Skift kategori for en ticket")
    @discord.app_commands.choices(
        category=[
            discord.app_commands.Choice(name=cat['name'], value=cat['value'])
            for cat in _category_cache.values()
        ]
    )
    async def switch(self, interaction: discord.Interaction, category: discord.app_commands.Choice[str]):
        access = Permission(interaction.user, Settings.get('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return

        ticket = Database.get({'channel_id': str(interaction.channel.id)})
        if not ticket:
            await interaction.response.send_message(
                "Denne ticket findes ikke i databasen. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return

        old_category = _category_cache.get(ticket['category'])
        selected_category = _category_cache.get(category.value)
        if not selected_category:
            await interaction.response.send_message(
                "Den valgte kategori findes ikke.",
                ephemeral=True
            )
            return
        
        newRole = interaction.guild.get_role(int(selected_category['role_access'])) if selected_category.get('role_access') else None
        oldRole = interaction.guild.get_role(int(old_category['role_access'])) if old_category.get('role_access') else None

        overwrites = interaction.channel.overwrites
        if newRole:
            overwrites[newRole] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        if oldRole:
            del overwrites[oldRole]

        await interaction.channel.edit(category=interaction.guild.get_channel(int(selected_category['channel_category'])), overwrites=overwrites)

        Database.update(interaction.channel.id,{
            'category': category.value
        })

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Pacific - Ticket System",
                description=(
                    f"**Ticket ID:** `{ticket['id']}`\n"
                    f"**Kategori skiftet til:** {selected_category['name']}\n"
                    f"**Skiftet af:** {interaction.user.mention}\n\n"
                    "Hvis du har spørgsmål eller brug for hjælp, så opret en ticket her: <#{}>.".format(Settings.get('ticket_channel'))
                ),
                color=discord.Color.blue()
            ).set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )
        )