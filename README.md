# 🚀 Telegram Channel Post Auto-Forward Bot

An automated Telegram bot built with Node.js that automatically forwards posts from a source channel to destination channels in real-time.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-v16+-green.svg)](https://nodejs.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram&logoColor=white)](https://t.me/BotFather)

---

## ✨ Features

- ⚡ **Instant Forwarding:** Automatically forwards new posts as soon as they are published.
- 🎯 **Multi-Channel Support:** Easily forward messages from one source channel to target channels.
- 📜 **Activity Logging:** Automatically logs post history and status in `forward.log`.
- 🛠️ **Lightweight & Fast:** Minimal setup with very low RAM and CPU consumption.

---

## 🛠️ Setup Guide

### Step 1: Create Your Bot & Get Channel IDs
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the steps to create a new bot.
3. Copy your **Bot Access Token** (Keep it secret!).
4. Add your bot as an **Admin** in both source and destination channels with **Manage Messages / Post Messages** permissions enabled.
5. Forward any post from your target channels to [@userinfobot](https://t.me/userinfobot) to get your **Channel IDs** (e.g., `-100123456789`).

---

### Step 2: Installation

Clone the repository and install all required dependencies:

```bash
git clone https://github.com/BidyutRoy2/tgpost.git
cd tgpost
npm install
```

### Step 3: Environment Configuration
Create or edit the .env file to configure your Bot Token and Channel IDs:
```
nano .env
```
Add your credentials inside .env:
Code snippet
```
BOT_TOKEN=your_bot_access_token_here
SOURCE_CHANNEL_ID=-100123456789
TARGET_CHANNEL_ID=-100987654321,100987654321,100987654321,Add More
```

###Step 4: Run the Bot Start the bot locally:
```
npm start
```

### To stop the bot in your terminal, press: CTRL + C

### 💡 Tip (Run 24/7 on Server): To keep the bot running permanently in the background, use PM2:

```
npm install -g pm2
pm2 start index.js --name "tg-forward-bot"
```

📄 License : Distributed under the MIT License.
