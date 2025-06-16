import discord

from src.events.ticket.buttons.call import TicketCall as Call
from src.events.ticket.buttons.close import TicketClose as Close
from src.events.ticket.buttons.claim import TicketClaim as Claim
from src.events.ticket.buttons.unclaim import TicketUnclaim as Unclaim
from src.events.ticket.transcript import Transcript as Transcript
from src.utils.ticket.dropdown.select import CategorySelect as SelectDropdown
from src.utils.ticket.dropdown.manager import SettingsDropdown as ManageDropdown
class Events():
    @staticmethod
    async def load(bot):
        view = discord.ui.View(timeout=None)
        view.add_item(SelectDropdown())
        view.add_item(ManageDropdown())
        bot.add_view(view)
        
        bot.add_view(Call())
        bot.add_view(Unclaim())
        bot.add_view(Claim())
        bot.add_view(Close())
        await bot.add_cog(Transcript())