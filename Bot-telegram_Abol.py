import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات خود را اینجا وارد کنید
TOKEN = '8027818270:AAET839KBqSoeletzMV3IGW2kynRPoMn540'

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دیکشنری برای ذخیره تعداد اخطارهای کاربران
user_warnings = {}

# لیست کلمات نامناسب
BAD_WORDS = ["کلمه1", "کلمه2", "کلمه3"]

# دستور شروع /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('سلام! من یک ربات مدیریت گروه پیشرفته هستم.')

# دستور حذف پیام /delete
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.message.reply_to_message.delete()
        await update.message.reply_text('پیام حذف شد.')
    else:
        await update.message.reply_text('لطفاً روی پیامی که می‌خواهید حذف کنید ریپلای کنید.')

# دستور محدود کردن کاربر /restrict
async def restrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text('کاربر محدود شد.')
    else:
        await update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید محدود کنید ریپلای کنید.')

# دستور آزاد کردن کاربر /unrestrict
async def unrestrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text('کاربر آزاد شد.')
    else:
        await update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید آزاد کنید ریپلای کنید.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("delete", delete_message))
    application.add_handler(CommandHandler("restrict", restrict_user))
    application.add_handler(CommandHandler("unrestrict", unrestrict_user))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
