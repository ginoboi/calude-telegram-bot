import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load API keys from environment
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Store conversation history per user (in-memory)
user_histories: dict[int, list] = {}

MAX_HISTORY = 20  # Max messages to keep per user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hi {user}! I'm your personal Claude AI assistant.\n\n"
        "Just send me a message and I'll respond. I remember our conversation context too!\n\n"
        "Commands:\n"
        "/start – Show this message\n"
        "/clear – Clear our conversation history\n"
        "/help – Tips on how to use me"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Tips for talking to me:*\n\n"
        "• Ask me anything — questions, tasks, writing, coding\n"
        "• I remember our conversation within a session\n"
        "• Use /clear to start a fresh conversation\n"
        "• I work best with clear, specific requests\n\n"
        "Go ahead, ask me something! 🚀",
        parse_mode="Markdown"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("🧹 Conversation cleared! Let's start fresh.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})

    if len(user_histories[user_id]) > MAX_HISTORY:
        user_histories[user_id] = user_histories[user_id][-MAX_HISTORY:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=(
                "You are a helpful, friendly AI assistant. "
                "Keep responses concise and conversational since this is a Telegram chat. "
                "Use plain text — avoid heavy markdown formatting."
            ),
            messages=user_histories[user_id],
        )

        reply = response.content[0].text
        user_histories[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error calling Claude API: {e}")
        await update.message.reply_text(
            "⚠️ Sorry, I ran into an issue. Please try again in a moment."
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
