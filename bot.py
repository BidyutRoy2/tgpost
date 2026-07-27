import os
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")
TARGET_CHANNELS_RAW = os.getenv("TARGET_CHANNELS", "")
FORWARD_DELAY_MS = int(os.getenv("FORWARD_DELAY", "10000"))

TARGET_CHANNELS = [cid.strip() for cid in TARGET_CHANNELS_RAW.split(",") if cid.strip()]
DELAY_SECONDS = FORWARD_DELAY_MS / 1000.0

POSTED_FILE = "posted.json"

def load_posted():
    if os.path.exists(POSTED_FILE):
        try:
            with open(POSTED_FILE, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_posted(posted_ids):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_ids[-100:], f, indent=4)

async def main():
    if not BOT_TOKEN or not MAIN_CHANNEL_ID or not TARGET_CHANNELS:
        print("Missing required environment variables!")
        return

    bot = Bot(token=BOT_TOKEN)
    posted_ids = load_posted()

    # ১. মেইন চ্যানেলের লেটেস্ট পোস্টের ID বের করার চেষ্টা
    latest_msg_id = None
    try:
        updates = await bot.get_updates(limit=50)
        for u in reversed(updates):
            msg = u.channel_post or u.edited_channel_post
            if msg and str(msg.chat.id) == str(MAIN_CHANNEL_ID):
                latest_msg_id = msg.message_id
                break
    except Exception as e:
        print(f"Update check error: {e}")

    # আপডেটসে না পাওয়া গেলে posted.json বা ডিফল্ট ৫০০ থেকে চেক করবে
    if not latest_msg_id:
        start_id = max(posted_ids) if posted_ids else 500
    else:
        start_id = latest_msg_id - 5

    print(f"Scanning messages starting from ID: {start_id}")

    # ২. মেসেজ আইডি রেঞ্জ চেক করা (গত ১০টি মেসেজ আইডি)
    for msg_id in range(start_id, start_id + 15):
        if msg_id in posted_ids:
            continue

        forwarded_count = 0
        for target_id in TARGET_CHANNELS:
            try:
                await bot.forward_message(
                    chat_id=target_id,
                    from_chat_id=MAIN_CHANNEL_ID,
                    message_id=msg_id
                )
                print(f"-> Successfully forwarded ID {msg_id} to {target_id}")
                forwarded_count += 1
                await asyncio.sleep(DELAY_SECONDS)
            except TelegramError as e:
                # পোস্ট না থাকলে বা প্রাইভেট চ্যানেলের রেস্ট্রিকশন থাকলে
                pass

        if forwarded_count > 0:
            posted_ids.append(msg_id)

    save_posted(posted_ids)

if __name__ == "__main__":
    asyncio.run(main())
