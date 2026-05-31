# Claude Telegram Bot

A Telegram bot powered by Claude AI (claude-sonnet-4-20250514). Supports multi-turn conversations with per-user history.

## Files
- `bot.py` – Main bot code
- `requirements.txt` – Python dependencies
- `Procfile` – Tells Railway how to run the bot

## Deploy to Railway (Free)

### 1. Put these files on GitHub
- Create a free account at https://github.com
- Create a new repository (e.g. `claude-telegram-bot`)
- Upload all 3 files: `bot.py`, `requirements.txt`, `Procfile`

### 2. Deploy on Railway
- Go to https://railway.app and sign in with GitHub
- Click **New Project → Deploy from GitHub Repo**
- Select your repository
- Click **Deploy**

### 3. Set Environment Variables (your API keys)
In Railway, go to your project → **Variables** tab → add:

| Variable Name      | Value                        |
|--------------------|------------------------------|
| `TELEGRAM_TOKEN`   | Your token from @BotFather   |
| `ANTHROPIC_API_KEY`| Your key from console.anthropic.com |

### 4. Redeploy
After adding variables, Railway will automatically redeploy. Your bot will be live!

## Commands
- `/start` – Welcome message
- `/help` – Usage tips  
- `/clear` – Clear conversation history

## Notes
- Conversation history is stored in memory (resets on restart)
- Max 20 messages kept per user to avoid token limits
- Free Railway tier gives 500 hours/month — enough for personal use
