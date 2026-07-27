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
                return json.load(f)
        except Exception:
            return []
    return []

def save_posted(posted_ids):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_ids, f, indent=4)

async def main():
    if not BOT_TOKEN or not MAIN_CHANNEL_ID or not TARGET_CHANNELS:
        print("Missing required environment variables!")
        return

    bot = Bot(token=BOT_TOKEN)
    posted_ids = load_posted()
    new_posted = list(posted_ids)

    try:
        # মেইন চ্যানেলের শেষ আপডেট দেখা
        updates = await bot.get_updates(offset=-10)
        
        for update in updates:
            # চ্যানেল পোস্ট বা এডিটেড পোস্ট চেক
            message = update.channel_post or update.edited_channel_post
            
            if not message:
                continue

            # পোস্টটি যদি নির্দিষ্ট মেইন চ্যানেল থেকে হয়
            if str(message.chat.id) == str(MAIN_CHANNEL_ID):
                msg_id = message.message_id

                if msg_id in posted_ids:
                    continue

                print(f"Forwarding message ID: {msg_id}")

                # প্রতিটি টার্গেট চ্যানেলে ফরোয়ার্ড করা
                for target_id in TARGET_CHANNELS:
                    try:
                        await bot.forward_message(
                            chat_id=target_id,
                            from_chat_id=MAIN_CHANNEL_ID,
                            message_id=msg_id
                        )
                        print(f"Successfully forwarded to {target_id}")
                    except TelegramError as e:
                        print(f"Failed to forward to {target_id}: {e}")

                    # সেটআপ করা ডিলে (10000ms = 10s)
                    await asyncio.sleep(DELAY_SECONDS)

                new_posted.append(msg_id)

    except Exception as e:
        print(f"Error checking updates: {e}")

    save_posted(new_posted)

if __name__ == "__main__":
    asyncio.run(main())
