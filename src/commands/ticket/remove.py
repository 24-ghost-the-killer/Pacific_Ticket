import discord
from discord.ext import commands

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="remove", description="Remove a user from the ticket")
    async def remove(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Remove(bot))
