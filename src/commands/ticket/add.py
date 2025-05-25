import discord
from discord.ext import commands

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="add", description="Add a user to the ticket")
    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(Add(bot))
