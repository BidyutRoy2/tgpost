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
        # শুধু শেষ ১০০টি আইডি সেভ রাখবে যাতে ফাইল ভারী না হয়
        json.dump(posted_ids[-100:], f, indent=4)

async def main():
    if not BOT_TOKEN or not MAIN_CHANNEL_ID or not TARGET_CHANNELS:
        print("Missing required environment variables!")
        return

    bot = Bot(token=BOT_TOKEN)
    posted_ids = load_posted()
    
    # লাস্ট সেভ করা মেসেজ আইডি থেকে চেক শুরু করবে
    last_id = max(posted_ids) if posted_ids else 1
    
    # বর্তমান রান-এ নতুন ৫-১০টি সম্ভাব্য মেসেজ আইডি স্ক্যান করবে
    found_any = False
    
    for msg_id in range(last_id, last_id + 15):
        if msg_id in posted_ids and msg_id != last_id:
            continue

        # যেকোনো একটি টার্গেট চ্যানেলে টেস্ট ফরোয়ার্ড করার চেষ্টা করবে
        forward_success = False
        for target_id in TARGET_CHANNELS:
            try:
                await bot.forward_message(
                    chat_id=target_id,
                    from_chat_id=MAIN_CHANNEL_ID,
                    message_id=msg_id
                )
                print(f"Successfully forwarded message {msg_id} to {target_id}")
                forward_success = True
                await asyncio.sleep(DELAY_SECONDS)
            except TelegramError as e:
                # মেসেজ না থাকলে বা অন্য এরর হলে
                pass

        if forward_success:
            found_any = True
            if msg_id not in posted_ids:
                posted_ids.append(msg_id)

    if not found_any:
        print("No new message found to forward.")

    save_posted(posted_ids)

if __name__ == "__main__":
    asyncio.run(main())
