import logging
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن ربات خود را اینجا وارد کنید
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دیکشنری برای ذخیره تعداد اخطارهای کاربران
user_warnings = {}

# لیست کلمات نامناسب
BAD_WORDS = ["کلمه1", "کلمه2", "کلمه3"]

# دستور شروع /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! من یک ربات مدیریت گروه پیشرفته هستم.')

# دستور حذف پیام /delete
def delete_message(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        update.message.reply_to_message.delete()
        update.message.reply_text('پیام حذف شد.')
    else:
        update.message.reply_text('لطفاً روی پیامی که می‌خواهید حذف کنید ریپلای کنید.')

# دستور محدود کردن کاربر /restrict
def restrict_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        update.message.reply_text('کاربر محدود شد.')
    else:
        update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید محدود کنید ریپلای کنید.')

# دستور آزاد کردن کاربر /unrestrict
def unrestrict_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        update.message.reply_text('کاربر آزاد شد.')
    else:
        update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید آزاد کنید ریپلای کنید.')

# دستور اخراج کاربر /kick
def kick_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        context.bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
        update.message.reply_text('کاربر اخراج شد.')
    else:
        update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید اخراج کنید ریپلای کنید.')

# دستور اضافه کردن کاربر /add
def add_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
        update.message.reply_text('کاربر اضافه شد.')
    else:
        update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید اضافه کنید ریپلای کنید.')

# دستور اخطار دادن به کاربر /warn
def warn_user(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        if user_id in user_warnings:
            user_warnings[user_id] += 1
        else:
            user_warnings[user_id] = 1

        if user_warnings[user_id] >= 3:
            kick_user(update, context)
            update.message.reply_text(f'کاربر به دلیل دریافت ۳ اخطار اخراج شد.')
            user_warnings[user_id] = 0
        else:
            update.message.reply_text(f'کاربر اخطار دریافت کرد. تعداد اخطارها: {user_warnings[user_id]}')
    else:
        update.message.reply_text('لطفاً روی پیام کاربری که می‌خواهید اخطار دهید ریپلای کنید.')

# فیلتر کردن کلمات نامناسب
def filter_bad_words(update: Update, context: CallbackContext):
    message_text = update.message.text
    if any(bad_word in message_text for bad_word in BAD_WORDS):
        update.message.delete()
        update.message.reply_text('پیام شما به دلیل استفاده از کلمات نامناسب حذف شد.')

# بررسی دسترسی ادمین
def is_admin(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    chat_member = context.bot.get_chat_member(chat_id, user_id)
    return chat_member.status in ['administrator', 'creator']

# دستورات فقط برای ادمین‌ها
def admin_only(handler):
    def wrapper(update: Update, context: CallbackContext):
        if is_admin(update, context):
            return handler(update, context)
        else:
            update.message.reply_text('شما دسترسی لازم برای اجرای این دستور را ندارید.')
    return wrapper

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # اضافه کردن دستورات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("delete", admin_only(delete_message)))
    dp.add_handler(CommandHandler("restrict", admin_only(restrict_user)))
    dp.add_handler(CommandHandler("unrestrict", admin_only(unrestrict_user)))
    dp.add_handler(CommandHandler("kick", admin_only(kick_user)))
    dp.add_handler(CommandHandler("add", admin_only(add_user)))
    dp.add_handler(CommandHandler("warn", admin_only(warn_user)))

    # فیلتر کردن کلمات نامناسب
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_bad_words))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()