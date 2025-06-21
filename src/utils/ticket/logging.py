import discord
from src.database.functions.settings import DatabaseSettings as Settings

class Logging:
    def __init__(self):
        self.logging_id = int(Settings.get('logging_channel'))

    async def close(self, interaction: discord.Interaction, data={ 'close_reason': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | CLOSE**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Lukket af:** {interaction.user.mention}.\n"
                f"```{data.get('close_reason', 'Ingen Grund')}```"
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    async def rename(self, interaction: discord.Interaction, data={ 'name': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | RENAME**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Ændret af:** {interaction.user.mention}.\n"
                f"```{data.get('name', 'Intet Navn')}```"
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    async def add(self, interaction: discord.Interaction, data={ 'user': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))
        added_user = interaction.guild.get_member(int(data.get('user')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | ADD**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Tilføjet af:** {interaction.user.mention}.\n\n"
                f"**Bruger Tilføjet:** {added_user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return

    async def remove(self, interaction: discord.Interaction, data={ 'user': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))
        removed_user = interaction.guild.get_member(int(data.get('user')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | REMOVE**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Tilføjet af:** {interaction.user.mention}.\n\n"
                f"**Bruger Fjernet:** {removed_user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def claim(self, interaction: discord.Interaction, data={ 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | CLAIM**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Claimet af:** {interaction.user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def unclaim(self, interaction: discord.Interaction, data={ 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | UNCLAIM**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Unclaimet af:** {interaction.user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def switch(self, interaction: discord.Interaction, data={ 'category': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | SWITCH**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Nye Kategory:** {data.get('category', 'Ingen Kategory')}.\n"
                f"**Gamle Kategory:** {ticket.get('category', 'Ingen Kategory')}.\n"
                f"**Ændret af:** {interaction.user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def call(self, interaction: discord.Interaction, data={ 'reason': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | INDKALD**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Ejer:** {owner.mention}.\n"
                f"**Ændret af:** {interaction.user.mention}.\n"
                f"```{data.get('reason', 'Ingen Grund')}```"
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def owner(self, interaction: discord.Interaction, data={ 'user': None, 'ticket': None }):
        ticket = data.get('ticket', {})
        owner = interaction.guild.get_member(int(ticket.get('owner_id')))
        new_owner = interaction.guild.get_member(int(data.get('user')))

        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | OWNER**',
            description=(
                f"**ID:** `{ticket.get('id', 'Intet ID')}`.\n"
                f"**Nye Ejer:** {new_owner.mention}.\n"
                f"**Gamle Ejer:** {owner.mention}.\n"
                f"**Ændret af:** {interaction.user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return
    
    async def panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='**PACIFIC - TICKET SYSTEM | PANEL**',
            description=(
                f"**Kanal:** {interaction.channel.mention}.\n"
                f"**Ændret af:** {interaction.user.mention}."
            ),
            color=discord.Color.blue(),
        ).set_footer(
            text=f"Pacific • Ticket System • {interaction.created_at.strftime('%d-%m-%Y %H:%M')}",
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )

        channel = interaction.guild.get_channel(self.logging_id)
        await channel.send(embed=embed)
        return