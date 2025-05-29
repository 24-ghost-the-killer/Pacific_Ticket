import discord

from src.events.ticket.call import TicketCall as Call
from src.events.ticket.close import TicketClose as Close
from src.events.ticket.claim import TicketClaim as Claim
from src.events.ticket.unclaim import TicketUnclaim as Unclaim
from src.utils.ticket.dropdown import TicketDropdown as Dropdown
class Events():
    @staticmethod
    async def view(bot):
        view = discord.ui.View(timeout=None)
        view.add_item(Dropdown())
        bot.add_view(view)
        bot.add_view(Call())
        bot.add_view(Unclaim())
        bot.add_view(Claim())
        bot.add_view(Close())
