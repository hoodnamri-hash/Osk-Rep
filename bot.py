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

# إعدادات البوت
TOKEN = "8356449349:AAHGWKhn6WrhpY3QHmO9fmg1oYDLtVAYBHo"
expiration_date = datetime(2028, 12, 31)

if datetime.now() > expiration_date:
    print("\033[1;32mTool Disabled by 777 \033[0m")
    exit()

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
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=f"reason_id={reason_id}&source_name=profile",
        )

        return report.status_code
    except Exception as e:
        return str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """بدء المحادثة وإرسال رسالة الترحيب."""
    user = update.message.from_user
    console.print(f"بدأ المستخدم {user.first_name} المحادثة")
    
    await update.message.reply_text(
        "مرحبًا بك في نظام Team 777! 👋\n\n"
        "يرجى إدخال اسم مستخدم Instagram للبدء.\n\n"
        "أرسل /cancel لإلغاء العملية في أي وقت.",
    )

    return USERNAME

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على اسم المستخدم."""
    username = update.message.text
    context.user_data['username'] = username
    
    await update.message.reply_text(
        f"تم حفظ اسم المستخدم: {username}\n\n"
        "الآن يرجى إدخال كلمة المرور الخاصة بـ Instagram:",
        reply_markup=ReplyKeyboardRemove()
    )

    return PASSWORD

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على كلمة المرور."""
    password = update.message.text
    context.user_data['password'] = password
    
    # إنشاء لوحة المفاتيح للاختيار
    reply_keyboard = [["تقرير حساب", "تقرير منشور"]]
    
    await update.message.reply_text(
        "تم تسجيل بيانات الدخول بنجاح! ✅\n\n"
        "الآن اختر نوع التقرير الذي تريد إنشاءه:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True,
            input_field_placeholder="اختر نوع التقرير"
        ),
    )

    return CHOICE

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """معالجة اختيار نوع التقرير."""
    choice_text = update.message.text
    context.user_data['choice'] = choice_text
    
    if choice_text == "تقرير حساب":
        await update.message.reply_text(
            "أدخل معرف المستخدم المستهدف (User ID):",
            reply_markup=ReplyKeyboardRemove()
        )
        return TARGET_ACCOUNT
    else:
        await update.message.reply_text(
            "أدخل رابط المنشور أو الرمز المختصر (shortcode):",
            reply_markup=ReplyKeyboardRemove()
        )
        return TARGET_POST

async def target_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على معرف الحساب المستهدف."""
    target_id = update.message.text
    context.user_data['target_id'] = target_id
    
    # إنشاء لوحة المفاتيح لأسباب التقرير
    reply_keyboard = [
        ["1 - Spam", "2 - Self-Injury"],
        ["3 - Drugs", "4 - Nudity"],
        ["5 - Violence", "6 - Hate Speech"],
        ["7 - Bullying", "8 - Impersonation"],
        ["9 - Underage"]
    ]
    
    await update.message.reply_text(
        f"تم تحديد المستهدف: {target_id}\n\n"
        "الآن اختر سبب التقرير:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True
        )
    )
    
    return REASON_ACCOUNT

async def reason_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على سبب التقرير للحساب."""
    reason_text = update.message.text
    reason_id = int(reason_text.split(" - ")[0])
    context.user_data['reason_id'] = reason_id
    
    await update.message.reply_text(
        f"بدأ عملية الإبلاغ عن الحساب...\n"
        f"الهدف: {context.user_data['target_id']}\n"
        f"السبب: {reason_text}\n\n"
        "جاري البدء، يرجى الانتظار...",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # بدء عملية الإبلاغ
    await start_reporting_account(update, context)
    
    return ConversationHandler.END

async def target_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على رابط المنشور المستهدف."""
    post_input = update.message.text.strip()
    context.user_data['post_input'] = post_input
    
    # استخراج الرمز المختصر من الرابط إذا كان رابطًا
    match = re.search(r"instagram\.com/p/([a-zA-Z0-9_-]+)/", post_input)
    shortcode = match.group(1) if match else post_input
    context.user_data['shortcode'] = shortcode
    
    # إنشاء لوحة المفاتيح لأسباب التقرير للمنشور
    reply_keyboard = [
        ["1 - Spam", "2 - Nudity"],
        ["3 - Violence", "4 - Hate Speech"],
        ["5 - Bullying", "6 - False Information"]
    ]
    
    await update.message.reply_text(
        f"تم تحديد المنشور: {shortcode}\n\n"
        "الآن اختر سبب التقرير:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True
        )
    )
    
    return REASON_POST

async def reason_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """الحصول على سبب التقرير للمنشور."""
    reason_text = update.message.text
    reason_id = int(reason_text.split(" - ")[0])
    context.user_data['reason_id'] = reason_id
    
    await update.message.reply_text(
        f"بدأ عملية الإبلاغ عن المنشور...\n"
        f"المنشور: {context.user_data['shortcode']}\n"
        f"السبب: {reason_text}\n\n"
        "جاري البدء، يرجى الانتظار...",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # بدء عملية الإبلاغ
    await start_reporting_post(update, context)
    
    return ConversationHandler.END

async def start_reporting_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية الإبلاغ عن الحساب."""
    user_data = context.user_data
    username = user_data['username']
    password = user_data['password']
    target_id = user_data['target_id']
    reason_id = user_data['reason_id']
    
    # محاولة تسجيل الدخول
    uid = str(uuid.uuid4())
    
    try:
        r1 = post(
            "https://i.instagram.com/api/v1/accounts/login/",
            headers={
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "i.instagram.com",
            },
            data={
                "_uuid": uid,
                "password": password,
                "username": username,
                "device_id": uid,
                "from_reg": "false",
                "_csrftoken": "missing",
                "login_attempt_count": "0",
            },
            allow_redirects=True,
        )

        if "logged_in_user" in r1.text:
            sessionid = r1.cookies["sessionid"]
            csrftoken = r1.cookies["csrftoken"]
            
            counter = 0
            success_count = 0
            
            # إرسال رسالة بدء العملية
            message = await update.message.reply_text(
                f"✅ تم تسجيل الدخول بنجاح!\n"
                f"جاري إرسال التقارير إلى الحساب المستهدف...\n\n"
                f"عدد التقارير المرسلة: 0\n"
                f"الحالة: جاري العمل..."
            )
            
            # بدء إرسال التقارير
            while counter < 20:  # حد أقصى 20 تقرير لأسباب أمنية
                counter += 1
                delay = random.uniform(2.5, 6.5)
                status = Report_Instagram(target_id, sessionid, csrftoken, reason_id)
                
                if str(status) == "200":
                    success_count += 1
                
                # تحديث الرسالة كل 5 تقارير
                if counter % 5 == 0 or counter == 1:
                    await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=message.message_id,
                        text=(
                            f"✅ جاري إرسال التقارير...\n\n"
                            f"عدد التقارير المرسلة: {counter}\n"
                            f"التقارير الناجحة: {success_count}\n"
                            f"آخر تأخير: {delay:.2f} ثانية\n"
                            f"آخر حالة: {status}"
                        )
                    )
                
                time.sleep(delay)
            
            # إرسال رسالة الانتهاء
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message.message_id,
                text=(
                    f"✅ اكتملت عملية الإبلاغ!\n\n"
                    f"إجمالي التقارير المرسلة: {counter}\n"
                    f"التقارير الناجحة: {success_count}\n"
                    f"نسبة النجاح: {(success_count/counter)*100:.2f}%"
                )
            )
            
        else:
            await update.message.reply_text(
                "❌ فشل تسجيل الدخول! يرجى التحقق من البيانات والمحاولة مرة أخرى."
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def start_reporting_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء عملية الإبلاغ عن المنشور."""
    user_data = context.user_data
    username = user_data['username']
    password = user_data['password']
    shortcode = user_data['shortcode']
    reason_id = user_data['reason_id']
    
    # محاولة تسجيل الدخول
    uid = str(uuid.uuid4())
    
    try:
        r1 = post(
            "https://i.instagram.com/api/v1/accounts/login/",
            headers={
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "i.instagram.com",
            },
            data={
                "_uuid": uid,
                "password": password,
                "username": username,
                "device_id": uid,
                "from_reg": "false",
                "_csrftoken": "missing",
                "login_attempt_count": "0",
            },
            allow_redirects=True,
        )

        if "logged_in_user" in r1.text:
            sessionid = r1.cookies["sessionid"]
            csrftoken = r1.cookies["csrftoken"]
            
            # الحصول على media_id من shortcode
            url = f"https://i.instagram.com/api/v1/media/shortcode/{shortcode}/info/"
            headers = {
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "cookie": f"sessionid={sessionid}",
            }

            res = get(url, headers=headers)
            if res.status_code != 200:
                await update.message.reply_text(
                    "❌ فشل في الحصول على معرّف المنشور. يرجى التحقق من الرابط والمحاولة مرة أخرى."
                )
                return

            media_id = res.json()["items"][0]["id"]
            
            counter = 0
            success_count = 0
            
            # إرسال رسالة بدء العملية
            message = await update.message.reply_text(
                f"✅ تم تسجيل الدخول بنجاح!\n"
                f"جاري إرسال التقارير إلى المنشور المستهدف...\n\n"
                f"عدد التقارير المرسلة: 0\n"
                f"الحالة: جاري العمل..."
            )
            
            # بدء إرسال التقارير
            while counter < 20:  # حد أقصى 20 تقرير لأسباب أمنية
                counter += 1
                delay = random.uniform(2.5, 6.5)
                status = Post_Report(sessionid, csrftoken, media_id, reason_id)
                
                if str(status) == "200":
                    success_count += 1
                
                # تحديث الرسالة كل 5 تقارير
                if counter % 5 == 0 or counter == 1:
                    await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=message.message_id,
                        text=(
                            f"✅ جاري إرسال التقارير...\n\n"
                            f"عدد التقارير المرسلة: {counter}\n"
                            f"التقارير الناجحة: {success_count}\n"
                            f"آخر تأخير: {delay:.2f} ثانية\n"
                            f"آخر حالة: {status}"
                        )
                    )
                
                time.sleep(delay)
            
            # إرسال رسالة الانتهاء
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message.message_id,
                text=(
                    f"✅ اكتملت عملية الإبلاغ!\n\n"
                    f"إجمالي التقارير المرسلة: {counter}\n"
                    f"التقارير الناجحة: {success_count}\n"
                    f"نسبة النجاح: {(success_count/counter)*100:.2f}%"
                )
            )
            
        else:
            await update.message.reply_text(
                "❌ فشل تسجيل الدخول! يرجى التحقق من البيانات والمحاولة مرة أخرى."
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """إلغاء المحادثة."""
    await update.message.reply_text(
        "تم إلغاء العملية.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة المساعدة."""
    await update.message.reply_text(
        "🆘 مساعدة بوت Team 777:\n\n"
        "🔹 /start - بدء عملية الإبلاغ\n"
        "🔹 /help - عرض رسالة المساعدة\n"
        "🔹 /cancel - إلغاء العملية الحالية\n\n"
        "لبدء عملية الإبلاغ عن حساب أو منشور على Instagram، استخدم الأمر /start"
    )

def main() -> None:
    """تشغيل البوت."""
    # إنشاء التطبيق وتمرير توكن البوت
    application = Application.builder().token(TOKEN).build()

    # إعداد معالج المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)],
            CHOICE: [MessageHandler(filters.Regex("^(تقرير حساب|تقرير منشور)$"), choice)],
            TARGET_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_account)],
            REASON_ACCOUNT: [MessageHandler(filters.Regex(r"^[1-9] - "), reason_account)],
            TARGET_POST: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_post)],
            REASON_POST: [MessageHandler(filters.Regex(r"^[1-6] - "), reason_post)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # إضافة معالجات الأوامر
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))

    # تشغيل البوت
    console.print("✅ بدأ تشغيل بوت Team 777...", style="bold green")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()