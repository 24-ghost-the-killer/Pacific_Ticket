import discord
from discord.ext import commands
from src.utils.ticket.database import TicketDatabase as Database
import os
import json
import datetime

class Transcript(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        ticket = Database.get({'channel_id': str(message.channel.id)})
        if not ticket:
            return

        transcript_entry = {
            'user': { 'name': message.author.name, 'id': str(message.author.id) },
            'content': { 'id': str(message.id), 'content': message.content },
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        if message.attachments:
            file_dir = f"data/{message.channel.id}/attachments"
            os.makedirs(file_dir, exist_ok=True)
            for attachment in message.attachments:
                file_path = os.path.join(file_dir, f"{message.id}_{attachment.filename}")
                await attachment.save(file_path)
                transcript_entry['files'] = transcript_entry.get('files', []) + [file_path]

        log_dir = f"data/{message.channel.id}"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "transcript.txt")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{transcript_entry['timestamp']}: {transcript_entry['user']}: {transcript_entry['content']}\n")
            if 'files' in transcript_entry:
                for file_path in transcript_entry['files']:
                    f.write(f"    [File]: {file_path}\n")

        existing_transcript = ticket.get('transcript', [])
        if isinstance(existing_transcript, str):
            try:
                existing_transcript = eval(existing_transcript)
                if not isinstance(existing_transcript, list):
                    existing_transcript = []
            except:
                existing_transcript = []

        updated_transcript = existing_transcript + [transcript_entry]
        serialized_transcript = json.dumps(updated_transcript)
        Database.update(message.channel.id, {
            'transcript': serialized_transcript
        })