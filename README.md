# Telegram Channel Post Auto Forward to Another Channel Bot

# Setup Guide
- Open Telegram Search https://t.me/BotFather
- Create a New Bot
- Copy Your Access Token (Don't Share)
- Copy Your Bot Username & Ad Admin Your All TG Channel (Manage Messaged - Post & Edit)
- Go To Your Main Channel & Otherrs
- Share Any Post `@userinfobot` To Get Channel ID

```
git clone https://github.com/BidyutRoy2/tgpost.git && cd tgpost
```
```
npm install
```
Edit .env File & Configure Your TG Bot Access Token and All ID
```
nano .env
```
Start Bot
```
npm start
```
To Stop
```
CRTL+C
```

# PROJECT STRUCTURE
- tgpost/
- ├── index.js
- ├── package.json
- ├── .env
- └── forward.log (Auto Created)
