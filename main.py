from telethon import TelegramClient, events
import random
from datetime import datetime
import asyncio
import os

# ===============================
# 🔐 API (Railway env support bhi)

api_id = int(os.getenv("API_ID", "36209925"))
api_hash = os.getenv("API_HASH", "59e1a8970239f845b05d7a5adc2e2af1")

client = TelegramClient("naiyer_session", api_id, api_hash)

# ===============================
# ⚙️ SETTINGS

busy_mode = True
replied_users = set()
custom_reply = None
vip_users = set()

# 😎 FLEX mono replies

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

    # VIP ignore
    if user_id in vip_users:
        return

    # ek user ko ek baar
    if user_id in replied_users:
        return

    replied_users.add(user_id)

    # typing animation
    async with client.action(event.chat_id, "typing"):
        await asyncio.sleep(2)

    # night check
    hour = datetime.now().hour
    if 23 <= hour or hour < 6:
        await event.reply(night_reply)
        return

    # custom ya random
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
