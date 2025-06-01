import discord
import datetime
from src.utils.ticket.database import TicketDatabase as Database
from src.database.main import Database as MainDatabase

class TicketCloseModel(discord.ui.Modal, title="Lukning af Ticket"):
    reason = discord.ui.TextInput(
        label="Årsag til lukning",
        style=discord.TextStyle.short,
        placeholder="Skriv her din årsag til at lukke ticketen...",
        required=True,
        max_length=50,
        custom_id="ticket_close_reason"
    )

    async def on_submit(self, interaction: discord.Interaction):
        ticket = Database().get({
            'channel_id': interaction.channel.id
        })
        
        owner = interaction.guild.get_member(int(ticket['owner_id']))
        if not owner:
            await interaction.response.send_message(
                "Ejeren af ticketen blev ikke fundet. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            f"Ticketen er bliver lukket om {MainDatabase.setting('close_time')} sekunder. Ejeren har fået besked.",
            ephemeral=True
        )
        close_time = int(MainDatabase.setting('close_time'))
        await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(seconds=close_time))
        await interaction.channel.delete(reason=f"Ticket lukket af {interaction.user} ({interaction.user.id})")

        embed = discord.Embed(
            title="**RadientRP - Ticket Lukket**",
            description=(
                f"Ticketen er blevet lukket af {interaction.user.mention}.\n"
                f"Du kan ikke længere sende beskeder i denne ticket.\n\n"
                f"**Ticket ID:** `{ticket['id']}`\n"
                f"**Lukket af:** {interaction.user.mention}\n"
                f"> {self.reason.value}"
            ),
            color=discord.Color.red(),
        )
        embed.set_footer(
            text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )

        try:
            await owner.send(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                "Jeg kunne ikke sende en besked til ejeren af ticketen. Sørg for, at de har direkte beskeder aktiveret.",
                ephemeral=True
            )
            return
        except Exception as e:
            await interaction.response.send_message(
                f"Der opstod en fejl under afsendelse af beskeden: {e}",
                ephemeral=True
            )
            return