
import os
import time
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Basic logging: never print the bot token
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

WEBAPP_URL = "https://givenchhund-droid.github.io/young-insta/"

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Set it before starting the bot.")

# Basic per-user rate limit
last_request = {}
RATE_LIMIT_SECONDS = 3


def is_rate_limited(user_id):
    now = time.time()
    previous = last_request.get(user_id, 0)

    if now - previous < RATE_LIMIT_SECONDS:
        return True

    last_request[user_id] = now
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user or not update.effective_chat:
        return

    if is_rate_limited(user.id):
        return

    if update.effective_chat.type != "private":
        await update.message.reply_text(
            "Please message Young Insta privately to use it."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "Open Young Insta 🖤",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ]
    ]

    await update.message.reply_text(
        "Welcome to Young Insta! 🖤\n\n"
        "Your social media dashboard is ready.\n"
        "Tap below to open it inside Telegram.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_rate_limited(update.effective_user.id):
        return

    await update.message.reply_text(
        "Young Insta Help 🖤\n\n"
        "/start - Open Young Insta\n"
        "/help - Show this help message\n\n"
        "Never share your Instagram password or verification codes."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        "An error occurred: %s",
        type(context.error).__name__ if context.error else "Unknown error",
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)

    logger.info("Young Insta is starting.")
    app.run_polling()


if __name__ == "__main__":
    main()

0
0

