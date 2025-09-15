import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ضع توكن البوت هنا
TOKEN = "8356449349:AAHGWKhn6WrhpY3QHmO9fmg1oYDLtVAYBHo"

# -------------------------
# أوامر البوت
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! البوت يعمل بنجاح.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب أي أمر لأتجاوب معك!")

# -------------------------
# رسالة عامة
# -------------------------

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هذا يرد بنفس الرسالة
    await update.message.reply_text(f"لقد كتبت: {update.message.text}")

# -------------------------
# الدالة الرئيسية لتشغيل البوت
# -------------------------

async def main():
    # إنشاء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    # تشغيل البوت باستخدام polling
    await app.run_polling()

# -------------------------
# تشغيل البوت
# -------------------------

if __name__ == "__main__":
    asyncio.run(main())
