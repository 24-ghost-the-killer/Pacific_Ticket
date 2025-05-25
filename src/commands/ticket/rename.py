import discord
from discord.ext import commands

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="rename", description="Rename the current ticket")
    async def rename(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Rename(bot))
