from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8410352881:AAFQeIkwcP2OiVidya8hHpqt5b_QxtDH-7Q"
CHANNEL = "@Songlio_ir"

async def is_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/Songlio_ir")],
            [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check")]
        ]
        await update.message.reply_text(
            "⚠️ برای استفاده از ربات باید عضو کانال شوید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text("🎵 خوش آمدید! اسم آهنگ را ارسال کنید.")

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_member(user_id, context):
        await query.message.edit_text("✅ عضویت تایید شد! حالا آهنگ بفرست 🎧")
    else:
        await query.answer("❌ هنوز عضو کانال نیستی", show_alert=True)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 در حال جستجو... (فعلاً تستی)")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

app.run_polling()