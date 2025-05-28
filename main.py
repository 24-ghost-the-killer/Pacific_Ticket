import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.database.main import Database
from src.commands.commands import Commands
from src.events.main import Events

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Connected to {bot.user.name} - {bot.user.id}')
    try:
        db = Database.connect()
        print('Connected to MySQL database successfully.')
        db.close()
    except Exception as e:
        print(f'Failed to connect to MySQL: {e}')
    await Commands.load(bot)
    await Events.view(bot)
    await bot.tree.sync()

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN not found in environment variables.")
    bot.run(TOKEN)
