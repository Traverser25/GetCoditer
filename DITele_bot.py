from telegram import Update, ParseMode
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext
)
from db_operation import SQLiteHandler

TECH, LOCATION, YOE = range(3)

TECH_LIST = [
    "Python", "Node.js", "React", "Django", "Flutter", "AWS", "GCP",
    "FastAPI", "MongoDB", "PostgreSQL", "MySQL"
]

user_state = {}

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_state[user_id] = {}

    tech_menu = "\n".join([f"{i+1}. {tech}" for i, tech in enumerate(TECH_LIST)])
    msg = f"👋 Welcome! Please select tech stack by replying with numbers (comma-separated):\n\n{tech_menu}"
    update.message.reply_text(msg)
    return TECH


def receive_techs(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text

    try:
        indices = [int(x.strip()) - 1 for x in text.split(",")]
        techs = [TECH_LIST[i] for i in indices if 0 <= i < len(TECH_LIST)]
    except Exception:
        update.message.reply_text("❌ Invalid input. Please reply like: `1,4,6`")
        return TECH

    user_state[user_id]["techs"] = techs
    update.message.reply_text("📍 Enter preferred location (or type `skip`):")
    return LOCATION

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("❌ Search cancelled.")
    return ConversationHandler.END
def receive_location(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    location = update.message.text.strip()

    if location.lower() == "skip":
        user_state[user_id]["location"] = None
    else:
        user_state[user_id]["location"] = location

    update.message.reply_text("🧠 Enter minimum years of experience (or type `skip`):")
    return YOE

def receive_yoe(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    if text == "skip":
        yoe = 0.0
    else:
        try:
            yoe = float(text)
        except:
            update.message.reply_text("❌ Invalid number. Please enter a numeric value or type `skip`.")
            return YOE

    user_state[user_id]["yoe"] = yoe
    techs = user_state[user_id]["techs"]
    location = user_state[user_id]["location"]

    # DB Query
    db = SQLiteHandler()
    results = db.filter_candidates(
        techs=techs,
        locations=[location] if location else None,
        min_yoe=yoe
    )

    if not results:
        update.message.reply_text("😞 No matching candidates found.")
        return ConversationHandler.END

    # Format and send results
    for i, candidate in enumerate(results[:10], 1):  # Limit to top 10
        msg = f"👤 *{candidate['author']}* ({candidate['experience_years']} yrs)\n"
        msg += f"📍 {candidate['location']} | 🧰 {', '.join(candidate['tech_stack'])}\n"
        if candidate["cv_link"]:
            msg += f"📄 [CV Link]({candidate['cv_link']})\n"
        msg += f"📝 {candidate['blurb'][:150]}...\n"  # Limit blurb length
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    db.close()

    return ConversationHandler.END


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TECH: [MessageHandler(Filters.text & ~Filters.command, receive_techs)],
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, receive_location)],
            YOE: [MessageHandler(Filters.text & ~Filters.command, receive_yoe)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
