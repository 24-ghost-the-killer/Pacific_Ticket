import discord
from discord.ext import commands
from src.database.functions.settings import DatabaseSettings as Settings

class VoiceRole(commands.Cog):
    def __init__(self):
        self.watched_channel_id = None
        self.role_id = None

    def _load_settings(self):
        if self.watched_channel_id is None:
            try:
                channel_id_str = Settings.get('support_channel')
                self.watched_channel_id = int(channel_id_str) if channel_id_str else 0
            except (ValueError, TypeError):
                print("Invalid 'support_channel' setting in database. This feature will be disabled.")
                self.watched_channel_id = 0

        if self.role_id is None:
            try:
                role_id_str = Settings.get('call_role')
                self.role_id = int(role_id_str) if role_id_str else 0
            except (ValueError, TypeError):
                print("Invalid 'call_role' setting in database. This feature will be disabled.")
                self.role_id = 0

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        self._load_settings()
        if not self.watched_channel_id or not self.role_id:
            return
            
        before_channel_id = before.channel.id if before.channel else None
        after_channel_id = after.channel.id if after.channel else None

        try:
            if before_channel_id == self.watched_channel_id and before_channel_id != after_channel_id:
                role = member.guild.get_role(self.role_id)
                if role in member.roles:
                    await member.remove_roles(role, reason="Left the special voice channel.")
        except discord.Forbidden:
            print(f"[VOICE ROLE DEBUG] Forbidden: Could not remove role from {member.display_name}. Check bot permissions.")
        except discord.HTTPException as e:
            print(f"[VOICE ROLE DEBUG] HTTPException: Failed to remove role: {e}")
        except Exception as e:
            print(f"[VOICE ROLE DEBUG] An error occurred in on_voice_state_update: {e}")