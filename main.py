import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from base_requests import get_response


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    telegram_id = user.id
    url = f"http://127.0.0.1:8000/api/user/telegram/{telegram_id}"
    response = await get_response(url)
    user_id = response["user_id"]
    if user_id == "not fount":
        await update.message.reply_html(f"Похоже вы, {user.mention_html()}, новый пользователь")
        await update.message.reply_text("Для начала работы пройдите небольшую регистрацию")





async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
