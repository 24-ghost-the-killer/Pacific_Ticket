import discord
from discord.ext import commands
from src.database.main import Database
from src.utils.permissions import Permission
class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add", description="Add a user to the ticket")
    async def add(self, interaction: discord.Interaction):
        access = Permission(interaction.user, Database.setting('support_role')).check()
        if not access:
            await interaction.response.send_message(
                "Du har ikke tilladelse til at bruge denne kommando.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")