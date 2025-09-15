import os
import re
import uuid
import time
import random
import logging
from datetime import datetime

from requests import post, get
from rich.console import Console
from colorist import Color

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# ⚠️ اجلب التوكن من متغير بيئة
TOKEN = os.getenv("BOT_TOKEN")  # ضعه في إعدادات Koyeb

# تعريف حالات المحادثة
USERNAME, PASSWORD, CHOICE, TARGET_ACCOUNT, REASON_ACCOUNT, TARGET_POST, REASON_POST = range(7)

console = Console()

class TextColor:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


# ========== دوال التقارير ==========
def Report_Instagram(target_id, sessionid, csrftoken, reportType):
    try:
        r3 = post(
            f"https://i.instagram.com/users/{target_id}/flag/",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Host": "i.instagram.com",
                "cookie": f"sessionid={sessionid}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=f"source_name=&reason_id={reportType}&frx_context=",
            allow_redirects=False,
        )
        return r3.status_code
    except Exception as e:
        return str(e)


def Post_Report(sessionid, csrftoken, media_id, reason_id):
    try:
        report_url = f"https://i.instagram.com/media/{media_id}/flag/"
        report = post(
            report_url,
            headers={
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "cookie": f"sessionid={sessionid}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=f"reason_id={reason_id}",
            allow_redirects=False,
        )
        return report.status_code
    except Exception as e:
        return str(e)


# ========== أوامر البوت ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا بوتك على تليجرام. اكتب /help لعرض المساعدة.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("الأوامر المتاحة:\n/start - بدء البوت\n/help - المساعدة")


# ========== main ==========
def main():
    if not TOKEN:
        raise ValueError("⚠️ لم يتم العثور على BOT_TOKEN في متغيرات البيئة.")

    application = Application.builder().token(TOKEN).build()

    # الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # شغل البوت
    application.run_polling()


if __name__ == "__main__":
    main()