import discord
from discord.ext import commands

class Switch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="switch", description="Switch to a different ticket category")
    async def switch(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Switch(bot))
