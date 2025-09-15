import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ضع توكن البوت هنا
TOKEN = "8356449349:AAHGWKhn6WrhpY3QHmO9fmg1oYDLtVAYBHo"
"

# مثال على أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! البوت يعمل بنجاح.")

# مثال على أمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب أي أمر لأتجاوب معك!")

async def main():
    # إنشاء التطبيق
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # تشغيل البوت (Polling)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
