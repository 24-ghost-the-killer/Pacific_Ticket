from discord.ext import commands
import os
import importlib
import asyncio
class Commands(commands.Cog):
    @staticmethod
    async def load(bot):
        ticket_dir = os.path.join(os.path.dirname(__file__), 'ticket')
        loaded = []
        for filename in os.listdir(ticket_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f"src.commands.ticket.{filename[:-3]}"
                module = importlib.import_module(module_name)
                if hasattr(module, 'setup'):
                    setup_func = getattr(module, 'setup')
                    if asyncio.iscoroutinefunction(setup_func):
                        await setup_func(bot)
                    else:
                        setup_func(bot)
                    loaded.append(filename)
        print(f"Loaded ticket commands: {', '.join(loaded) if loaded else 'None'}")