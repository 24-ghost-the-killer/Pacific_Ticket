import discord
from discord.ext import commands
from src.database.database import Database

class CategoryDropdown(discord.ui.Select):
    def __init__(self, categories):
        default_emoji = "📂"
        options = []
        for cat in categories:
            option_kwargs = {
                'label': cat['label'],
                'value': cat['value'],
                'description': cat.get('description')
            }
            emote = cat.get('emote')
            if emote:
                emote = emote.strip()
                if emote and len(emote) <= 2:
                    option_kwargs['emoji'] = emote
                else:
                    option_kwargs['emoji'] = default_emoji
            else:
                option_kwargs['emoji'] = default_emoji
            options.append(discord.SelectOption(**option_kwargs))
        super().__init__(placeholder=f"{default_emoji} Vælg en kategori...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]
        # Fetch the selected category from the database
        db = Database.connect()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorys WHERE value = %s", (selected_value,))
        category = cursor.fetchone()
        cursor.close()
        db.close()
        if not category:
            if not interaction.response.is_done():
                await interaction.response.send_message("Kategori ikke fundet.", ephemeral=True)
            return

        guild = interaction.guild
        # Set up permission overwrites
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        # Add access role if set
        role_access_id = category.get('role_access')
        if role_access_id:
            try:
                role = guild.get_role(int(role_access_id))
                if role:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
            except Exception:
                pass

        # Get the Discord category for the channel
        channel_category = None
        channel_category_id = category.get('channel_category')
        if channel_category_id:
            try:
                channel_category = guild.get_channel(int(channel_category_id))
                if channel_category and channel_category.type != discord.ChannelType.category:
                    channel_category = None
            except Exception:
                channel_category = None

        try:
            await interaction.response.defer(ephemeral=True)
        except Exception:
            pass
        # Create the channel
        try:
            channel_name = f"ticket-{interaction.user.name.lower()}"
            ticket_channel = await guild.create_text_channel(
                name=channel_name,
                overwrites=overwrites,
                category=channel_category,
                reason=f"Ticket for {interaction.user.display_name} ({selected_value})"
            )
            # Create an embed for the ticket channel
            ticket_embed = discord.Embed(
                title="🎫 RadientRP Ticket",
                description=f"Velkommen {interaction.user.mention}!\nEn supporter vil hjælpe dig snarest muligt.\n\nBrug knapperne nedenfor for at håndtere din ticket.",
                color=discord.Color.green()
            )
            ticket_embed.set_footer(text="RadientRP • Ticket System")
            # Create a view with buttons
            class TicketButtons(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, custom_id="ticket_claim")
                async def claim(self, button, interaction):
                    await interaction.response.send_message("Ticket claimed!", ephemeral=True)
                @discord.ui.button(label="Indkald", style=discord.ButtonStyle.secondary, custom_id="ticket_indkald")
                async def indkald(self, button, interaction):
                    await interaction.response.send_message("Staff is being called to this ticket!", ephemeral=True)
                @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="ticket_close")
                async def close(self, button, interaction):
                    await interaction.response.send_message("Ticket will be closed!", ephemeral=True)
            await ticket_channel.send(embed=ticket_embed, view=TicketButtons())
            await interaction.followup.send(f"Ticket oprettet: {ticket_channel.mention}", ephemeral=True)
            # Reset dropdown selection by sending a new view (replacing the old one)
            try:
                original_message = await interaction.channel.fetch_message(interaction.message.id)
                await original_message.edit(view=type(self.view)(self.view.children[0].options))
            except Exception:
                pass
        except discord.Forbidden:
            await interaction.followup.send("Jeg har ikke tilladelse til at oprette kanaler. Kontakt en admin.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Der opstod en fejl: {e}", ephemeral=True)

class PanelView(discord.ui.View):
    def __init__(self, categories):
        super().__init__(timeout=None)
        self.add_item(CategoryDropdown(categories))

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="panel", description="Create a new ticket panel")
    async def panel(self, interaction: discord.Interaction):
        db = Database.connect()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT label, value, emote, description FROM categorys")
        categories = cursor.fetchall()
        cursor.close()
        db.close()
        if not categories:
            await interaction.response.send_message("Ingen kategorier fundet i databasen.", ephemeral=True)
            return

        embed = discord.Embed(
            title="RadientRP - Ticket System",
            description=(
                "Hej og velkommen til RadientRP's ticket support!\n\n"
                "Vælg en kategori i menuen nedenfor for at oprette en ticket.\n"
                "Vores team står klar til at hjælpe dig hurtigt og professionelt.\n\n"
                "**Kategorier:**\n"
                "🔧 **Support:** Få hjælp til spørgsmål eller generelle problemer.\n"
                "🔓 **Unban:** Hjælp vedrørende FiveGuard eller TX bans.\n"
                "💰 **Donation:** Spørgsmål om donationer.\n"
                "👥 **Staff:** Kontakt vores staff."
            ),
            color=discord.Color.red()
        )
        embed.set_footer(
            text=f"RadientRP • Ticket Support • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url="https://radientrp.vercel.app/_next/image?url=%2Fradient_logo.png&w=128&q=75"
        )
        await interaction.response.send_message(embed=embed, view=PanelView(categories))

async def setup(bot):
    await bot.add_cog(Panel(bot))
