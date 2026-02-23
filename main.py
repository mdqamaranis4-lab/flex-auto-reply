from telethon import TelegramClient, events
import random
from datetime import datetime
import asyncio
import os
from telethon.sessions import StringSession

# ===============================
# 🔐 API + STRING_SESSION (Railway friendly)
api_id = int(os.getenv("API_ID"))                     # Name column me API_ID
api_hash = os.getenv("API_HASH")                     # Name column me API_HASH
string_session = os.getenv("STRING_SESSION")         # Name column me STRING_SESSION

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# ===============================
# ⚙️ SETTINGS
busy_mode = True
replied_users = set()
custom_reply = None
vip_users = set()

flex_replies = [
    "`Relax… F L A X busy hai. 😎 Main online aate hi reply kar dunga.`",
    "`Limitless mode ON… ⏳ F L A X thodi der me reply dega.`",
    "`Yo… message mil gaya. Wait karo zara. ⚡`",
    "`Itni jaldi kya hai? 😏 F L A X dekh raha hai.`",
    "`Main abhi busy hoon… par tum ignore nahi ho. ✨`"
]

night_reply = "`F L A X so raha hai… 🌙 Subah reply milega.`"

# ===============================
# 🤖 AUTO REPLY
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global busy_mode
    if not busy_mode:
        return
    user_id = event.sender_id
    if user_id in vip_users or user_id in replied_users:
        return
    replied_users.add(user_id)
    async with client.action(event.chat_id, "typing"):
        await asyncio.sleep(2)
    hour = datetime.now().hour
    if 23 <= hour or hour < 6:
        await event.reply(night_reply)
        return
    if custom_reply:
        await event.reply(f"`{custom_reply}`")
    else:
        await event.reply(random.choice(flex_replies))

# ===============================
# 🎮 COMMANDS
@client.on(events.NewMessage(outgoing=True, pattern=r"\.busy (on|off)"))
async def busy_handler(event):
    global busy_mode
    busy_mode = (event.pattern_match.group(1) == "on")
    await event.edit(f"✅ Busy mode {event.pattern_match.group(1).upper()}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.setreply (.+)"))
async def set_reply(event):
    global custom_reply
    custom_reply = event.pattern_match.group(1)
    await event.edit("✅ Custom auto-reply set ho gaya.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.vipadd (\d+)"))
async def vip_add(event):
    uid = int(event.pattern_match.group(1))
    vip_users.add(uid)
    await event.edit(f"✅ {uid} VIP me add ho gaya.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.vipdel (\d+)"))
async def vip_del(event):
    uid = int(event.pattern_match.group(1))
    vip_users.discard(uid)
    await event.edit(f"❌ {uid} VIP se remove ho gaya.")

# ===============================
print("😈 MONO F L A X GOD MODE chal raha hai...")
client.start()
client.run_until_disconnected()
