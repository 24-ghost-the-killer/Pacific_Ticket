import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.database.main import Database as Database
from src.database.functions.settings import SettingsDatabase as Settings

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="manage", description="Administrer indstillinger for ticket systemet")
    async def manage(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Settings.get('panel_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return

        settings = Settings.getall()

        class SettingsDropdown(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label=setting['name'], description=setting['value'], value=setting['value'])
                    for setting in settings if not setting['disabled']
                ]
                super().__init__(placeholder="Vælg en indstilling", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                selected_option = next(
                    (setting for setting in settings if setting['value'] == self.values[0]),
                    None
                )

                if not selected_option:
                    await interaction.response.send_message(
                        "Den valgte indstilling blev ikke fundet.",
                        ephemeral=True
                    )
                    return

                class TextInputModal(discord.ui.Modal):
                    def __init__(self, name, value):
                        super().__init__(title="Ændr indstilling")
                        self.label = name
                        self.add_item(
                            discord.ui.TextInput(
                                label=name,
                                default=value,
                                placeholder="Indtast ny værdi her"
                            )
                        )

                    async def on_submit(self, interaction: discord.Interaction):
                        new_value = self.children[0].value
                        Settings.update(
                            self.label,
                            new_value
                        )
                        await interaction.response.send_message(
                            f"Indstillingen '{self.label}' er blevet opdateret til: {new_value}",
                            ephemeral=True
                        )

                await interaction.response.send_modal(TextInputModal(selected_option['name'], selected_option['value']))

        class SettingsView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(SettingsDropdown())

        embed = discord.Embed(
            title="Manage Ticket",
            description="Vælg en indstilling fra dropdown-menuen nedenfor.",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=SettingsView(), ephemeral=True)