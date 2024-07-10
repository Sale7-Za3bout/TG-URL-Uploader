import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة البدء
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أرسل لي رابط URL لتحميل الملف.')

# دالة تحميل الملفات
def download_file(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        response = requests.get(url)
        response.raise_for_status()
        file_name = url.split("/")[-1]
        with open(file_name, 'wb') as file:
            file.write(response.content)
        update.message.reply_document(open(file_name, 'rb'))
        os.remove(file_name)
    except Exception as e:
        update.message.reply_text(f'حدث خطأ أثناء التحميل: {e}')

def main():
    # توكن البوت
    token = os.getenv("7338853071:AAHUW7jLGNs-7ZAReU1mBHc_OSx_HFpfrd0")
    updater = Updater(token)
    
    # إعداد المحاور
    dispatcher = updater.dispatcher

    # معالجة الأوامر
    dispatcher.add_handler(CommandHandler("start", start))

    # معالجة الرسائل النصية
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_file))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
