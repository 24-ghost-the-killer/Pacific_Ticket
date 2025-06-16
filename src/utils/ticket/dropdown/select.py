import discord
from src.events.ticket.buttons.call import TicketCall as Call
from src.events.ticket.buttons.close import TicketClose as Close
from src.events.ticket.buttons.claim import TicketClaim as Claim
from src.utils.ticket.database import TicketDatabase as Database
class CategorySelect(discord.ui.Select):
    def __init__(self):
        self._categories = None
        self._category_cache = {}
        self._role_cache = {}
        self._channel_category_cache = {}
        self._init_categories()
        if not self._categories:
            return {
                "error": True,
                "message": "Ingen kategorier tilgængelige. Opret venligst en kategori først."
            }
        options = []
        default_emote = "📂"

        for cat in self._categories:
            option_kwargs = {
                "label": cat['label'],
                "value": cat['value'],
                "description": cat.get('description') or "Ingen beskrivelse tilgængelig",
                "emoji": cat.get('emote', default_emote)
            }

            options.append(discord.SelectOption(**option_kwargs))
        super().__init__(
            placeholder="📂 Vælg en kategori",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_dropdown",
        )

    def _init_categories(self):
        if self._categories is None:
            self._categories = Database.categorys()

    def _get_category(self, value):
        if value in self._category_cache:
            return self._category_cache[value]
        cat = Database.category({'value': value})
        if cat:
            self._category_cache[value] = cat
        return cat

    def _get_channel_category(self, guild, channel_category_id):
        if channel_category_id in self._channel_category_cache:
            return self._channel_category_cache[channel_category_id]
        channel_category = guild.get_channel(int(channel_category_id))
        if channel_category and channel_category.type == discord.ChannelType.category:
            self._channel_category_cache[channel_category_id] = channel_category
            return channel_category
        return None

    def _get_role(self, guild, role_id):
        if role_id in self._role_cache:
            return self._role_cache[role_id]
        role = guild.get_role(int(role_id))
        if role:
            self._role_cache[role_id] = role
        return role

    async def callback(self, interaction: discord.Interaction):
        category = self._get_category(self.values[0])

        if not category:
            await interaction.response.send_message(
                "Der opstod en fejl under hentning af kategorien. Prøv venligst igen.",
                ephemeral=True
            )
            return

        channel_category = None
        if category['channel_category'] is None:
            await interaction.response.send_message(
                "Denne kategori er ikke tilknyttet en kanal. Kontakt venligst en administrator.",
                ephemeral=True
            )
            return
        elif category['channel_category']:
            try:
                channel_category = self._get_channel_category(interaction.guild, category['channel_category'])
                if not channel_category:
                    await interaction.response.send_message(
                        "Den angivne kanalkategori findes ikke. Kontakt venligst en administrator.",
                        ephemeral=True
                    )
                    return
            except Exception as e:
                await interaction.response.send_message(
                    f"Der opstod en fejl under oprettelse af ticket: {e}",
                    ephemeral=True
                )
                return
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            if category['role_access']:
                role = self._get_role(interaction.guild, category['role_access'])
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                else:
                    await interaction.response.send_message(
                        "Den angivne rolle findes ikke. Kontakt venligst en administrator.",
                        ephemeral=True
                    )
                    return
            channel = await interaction.guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                category=channel_category,
                topic=f"Ticket oprettet af {interaction.user.name} ({interaction.user.id})",
                reason=f"Ticket oprettet af {interaction.user.name} ({interaction.user.id}) for kategori {category['label']}",
                overwrites=overwrites
            )

            Database().create({
                'channel_name': channel.name,
                'channel_id': str(channel.id),
                'owner_username': interaction.user.name,
                'owner_id': str(interaction.user.id),
                'category': category['value']
            })  

            embed = discord.Embed(
                title = "Pacific - Ticket System",
                description = (
                    f"Hej {interaction.user.mention}, din ticket er oprettet!\n\n"
                    f"Kategori: {category['label']}\n"
                    "Vores personale vil snart være i kontakt med dig.\n\n"
                    "Hvis du har brug for hjælp, kan du kontakte en administrator."
                ),
                color=discord.Color.blue(),
            )
            embed.set_footer(
                text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )

            view = discord.ui.View(timeout=None)
            for button_cls in (Close, Claim, Call):
                view.add_item(button_cls().children[0])

            await channel.send(embed=embed,view=view)
            await interaction.response.defer()

            await interaction.followup.send(
                f"Din ticket er oprettet: {channel.mention}",
                ephemeral=True
            )

            try:
                dropdownMessage = await interaction.channel.fetch_message(interaction.message.id)
                view = discord.ui.View(timeout=None)
                view.add_item(CategorySelect())
                if dropdownMessage:
                    await dropdownMessage.edit(view=view)
            except discord.NotFound:
                pass
            except Exception as e:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"Der opstod en fejl under oprettelse af ticket: {e}",
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        f"Der opstod en fejl under oprettelse af ticket: {e}",
                        ephemeral=True
                    )
                return
        except discord.Forbidden:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "Jeg har ikke tilladelse til at oprette kanaler i denne server. Kontakt venligst en administrator.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "Jeg har ikke tilladelse til at oprette kanaler i denne server. Kontakt venligst en administrator.",
                    ephemeral=True
                )
            return
        except Exception as e:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"Der opstod en fejl under oprettelse af ticket: {e}",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"Der opstod en fejl under oprettelse af ticket: {e}",
                    ephemeral=True
                )
            return