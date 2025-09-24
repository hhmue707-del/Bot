# music_bot.py
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from yt_dlp import YoutubeDL
import asyncio

# ===== Bot credentials =====
api_id = 29799310           # my.telegram.org
api_hash = "3336adf6895c1d55e88873cef51dfb25"
bot_token = "8268848983:AAGePVO0P1cUVd6-0iGbbPIdKskJfEt7d4Q"

# ===== Setup Bot & PyTgCalls =====
app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
pytgcalls = PyTgCalls(app)

# ===== YouTube search function =====
def get_audio_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': 'in_playlist'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
        return info['url'], info['title']

# ===== Start command =====
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🎵 Music Bot is ready! Use /play song_name to play music in VC.")

# ===== Play command =====
@app.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("Please provide song name! Example: /play despacito")
        return
    
    song_name = " ".join(message.command[1:])
    msg = await message.reply_text(f"🔍 Searching for '{song_name}' on YouTube...")
    
    try:
        audio_url, title = get_audio_url(song_name)
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(InputAudioStream(audio_url))
        )
        await msg.edit_text(f"🎶 Now playing: {title}")
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")

# ===== Stop command =====
@app.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ Music stopped!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# ===== Run Bot =====
app.start()
pytgcalls.start()
print("Bot is running...")

asyncio.get_event_loop().run_forever()
