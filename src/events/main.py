import discord

from src.events.ticket.buttons.call import TicketCall as CallButton
from src.events.ticket.buttons.close import TicketClose as CloseButton
from src.events.ticket.buttons.claim import TicketClaim as ClaimButton
from src.events.ticket.buttons.unclaim import TicketUnclaim as UnclaimButton
from src.events.ticket.transcript import Transcript as Transcript
from src.events.ticket.call_remove import VoiceRole
from src.utils.ticket.dropdown.select import CategorySelect as SelectDropdown
from src.utils.ticket.dropdown.manager import SettingsDropdown as ManageDropdown

class Events():
    @staticmethod
    async def load(bot):
        try:
            view = discord.ui.View(timeout=None)
            view.add_item(SelectDropdown())
            view.add_item(ManageDropdown())
            bot.add_view(view)
            
            bot.add_view(CallButton())
            bot.add_view(UnclaimButton())
            bot.add_view(ClaimButton())
            bot.add_view(CloseButton())
            await bot.add_cog(Transcript())
            await bot.add_cog(VoiceRole())
        except discord.errors.NotFound as e:
            print(f"Error loading events: {e}")
            return
        except discord.errors.Forbidden as e:
            print(f"Error loading events: {e}")
            return
        except discord.errors.HTTPException as e:
            print(f"Error loading events: {e}")
            return
        except discord.errors.ClientException as e:
            print(f"Error loading events: {e}")
            return
        except Exception as e:
            print(f"Error loading events: {e}") 
            return