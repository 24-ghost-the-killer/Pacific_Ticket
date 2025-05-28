import discord
from src.utils.ticket.database import TicketDatabase as Database
import functools

class TicketModel(discord.ui.Modal, title="Indkald til support"):
    reason = discord.ui.TextInput(
        label="Årsag til indkaldelse",
        style=discord.TextStyle.paragraph,
        placeholder="Skriv her din årsag til at indkalde personen...",
        required=True,
        max_length=500,
        custom_id="ticket_reason"
    )

    @staticmethod
    @functools.lru_cache(maxsize=32)
    def call_role():
        from src.database.main import Database as MainDatabase
        return MainDatabase.setting('call_role')

    async def on_submit(self, interaction: discord.Interaction):
        ticket = Database().get({
            'channel_id': interaction.channel.id
        })

        if not ticket:
            await interaction.response.send_message(
                "Der opstod en fejl under hentning af data. Prøv venligst igen.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="**RadientRP - Support Indkaldelse**",
            description=(
                f"Du er blevet indkaldt til support fra en ticket på RadientRP.\n"
                f"Du kan tilgå din ticket her: {interaction.channel.jump_url}\n\n"
                f"**Ticket ID:** `{ticket['id']}`\n"
                f"**Indkaldt af:** {interaction.user.mention}\n"
                f"> {self.reason.value}"
            ),
            color=discord.Color.red(),
        )
        embed.set_footer(
            text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )

        owner = interaction.guild.get_member(int(ticket['owner_id']))
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
        
        call_role_id = self.call_role()
        if call_role_id is not None:
            role = interaction.guild.get_role(int(call_role_id))
            if role and owner:
                try:
                    await owner.add_roles(role, reason="Indkaldt til support via ticket system")
                except Exception as e:
                    await interaction.response.send_message(
                        f"Der opstod en fejl under tildeling af rolle: {e}",
                        ephemeral=True
                    )
                    return

        response_embed = discord.Embed(
            title="RadientRP - Support Indkaldelse",
            description=(
                f"{owner.mention} er blevet indkaldt til support!\n\n"
                f"**Indkaldt af:** {interaction.user.mention}\n"
                f"**Årsag:**\n> {self.reason.value}"
            ),
            color=discord.Color.red(),
        )
        response_embed.set_footer(
            text=f"RadientRP • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )
        await interaction.channel.send(embed=response_embed)
        await interaction.response.send_message(
            "Indkaldelse sendt! Ticket-ejeren har fået besked.",
            ephemeral=True
        )



