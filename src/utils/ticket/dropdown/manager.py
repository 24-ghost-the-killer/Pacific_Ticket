import discord
from src.database.functions.settings import DatabaseSettings as Settings

class SettingsDropdown(discord.ui.Select):
    def __init__(self):
        self.settings = Settings.getall()
        options = [
            discord.SelectOption(label=setting['name'], description=setting['value'], value=setting['value'])
            for setting in self.settings if not setting['disabled']
        ]
        super().__init__(
            placeholder="Vælg en indstilling", 
            min_values=1, 
            max_values=1,
            custom_id="settings_dropdown",
            options=options
)

    async def callback(self, interaction: discord.Interaction):
        selected_option = next(
            (setting for setting in self.settings if setting['value'] == self.values[0]),
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

                if Settings.get(self.label) == new_value:
                    await interaction.response.send_message(
                        f"Indstillingen `{self.label}` er allerede sat til: {new_value}",
                        ephemeral=True
                    )
                    return

                Settings.update(self.label, new_value)
                await interaction.response.send_message(
                    f"Indstillingen `{self.label}` er blevet opdateret til: {new_value}",
                    ephemeral=True
                )

        await interaction.response.send_modal(TextInputModal(selected_option['name'], selected_option['value']))