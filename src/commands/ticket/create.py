import discord
from discord.ext import commands

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="create", description="Create a new ticket")
    async def create(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Create(bot))
