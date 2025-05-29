import discord
from discord.ext import commands
from src.utils.permissions import Permission
from src.database.main import Database

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="remove", description="Remove a user from the ticket")
    async def remove(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Database.setting('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")