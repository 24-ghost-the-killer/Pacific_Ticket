from discord.ext import commands
import os
import importlib
class Commands(commands.Cog):
    @staticmethod
    async def load(bot):
        ticket_dir = os.path.join(os.path.dirname(__file__), 'ticket')
        loaded = []
        for filename in os.listdir(ticket_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f"src.commands.ticket.{filename[:-3]}"
                module = importlib.import_module(module_name)
                class_name = filename[:-3].capitalize()
                if hasattr(module, class_name):
                    cog_class = getattr(module, class_name)
                    if not issubclass(cog_class, commands.Cog):
                        print(f"Skipping {filename}: {class_name} is not a subclass of commands.Cog")
                    await bot.add_cog(cog_class(bot))
                    loaded.append(filename)
                else:
                    print(f"Skipping {filename}: {class_name} not found in module {module_name}")
        print(f"Loaded ticket commands: {', '.join(loaded) if loaded else 'None'}")