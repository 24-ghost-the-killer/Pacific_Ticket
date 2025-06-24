import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from src.database.main import Database
from src.commands.commands import Commands
from src.events.main import Events
from src.utils.ticket.database import TicketDatabase

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=10)
async def rich_presence():
    tickets = TicketDatabase.statistics()
    antal = tickets['opened']
    await bot.change_presence(
        activity=discord.CustomActivity(
            f"Behandler {antal} {"åben sag" if antal == 1 else "åbne sager"}!",
            emoji="🔎"
        )
    )

@bot.event
async def on_ready():
    print(f'Connected to {bot.user.name} - {bot.user.id}')
    try:
        conn = Database.connect()
        if conn:
            print('Connected to the database successfully.')
            conn.close()
        else:
            print('Failed to connect to the database.')
    except Exception as e:
        print(f'Failed to connect to MySQL: {e}')
    await Commands.load(bot)
    await Events.load(bot)
    await rich_presence.start()
    await bot.tree.sync()

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN not found in environment variables.")
    bot.run(TOKEN)
