import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from detect_intent_texts import detect_intent_texts


def start():
    load_dotenv(find_dotenv())
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dp = Dispatcher(bot)
    dp.register_message_handler(lambda message: send_message(message, bot))
    executor.start_polling(dp, skip_updates=True)


async def send_message(message: types.Message, bot: Bot):
    """Данная функция принимает сообщение пользователя и подбирает соответствующий Intent в качестве ответа"""
    session_id = str(message.from_user.id)
    response = detect_intent_texts(os.environ.get('PROJECT_ID'), session_id, message.text, 'ru')
    text = response.query_result.fulfillment_text
    await bot.send_message(chat_id=session_id, text=text)


# Start the bot
if __name__ == '__main__':
    start()
