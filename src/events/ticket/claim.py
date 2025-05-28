import discord

class TicketClaim(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.red, emoji="🎫", custom_id="ticket_claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Du har indkaldt support! En supporter vil hjælpe dig snart.", ephemeral=True)