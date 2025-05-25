import discord
from discord.ext import commands

class Close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="close", description="Close the current ticket")
    async def close(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Close(bot))
