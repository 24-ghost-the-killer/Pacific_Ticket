import discord
from discord.ext import commands

class Claim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="claim", description="Claim the current ticket")
    async def claim(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Claim(bot))
