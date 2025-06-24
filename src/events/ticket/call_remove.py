import discord
from discord.ext import commands
from src.database.functions.settings import DatabaseSettings as Settings

WATCHED_CHANNEL_ID = int(Settings.get('support_channel'))
ROLE_ID = int(Settings.get('call_role'))

class VoiceRole(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel and before.channel.id == WATCHED_CHANNEL_ID:
            if not after.channel or after.channel.id != WATCHED_CHANNEL_ID:
                try:
                    role = member.guild.get_role(ROLE_ID)
                    if role and role in member.roles:
                        await member.remove_roles(role, reason="Left the special voice channel.")
                except discord.Forbidden as e:
                    print(f"Forbidden: {e}. Jeg har ikke tilladelse til at fjerne rollen. Kontakt venligst en administrator.")
                    return
                except discord.HTTPException as e:
                    print(f"HTTPException: {e}. Der opstod en fejl. Prøv venligst igen senere.")
                    return
                except Exception as e:
                    print(f"Exception: {e}. Der opstod en uventet fejl.")
                    return