import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv, find_dotenv

from detect_intent_texts import detect_intent_texts


def start():
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dp = Dispatcher(bot)
    dp.register_message_handler(lambda message: send_message(message, bot))
    executor.start_polling(dp, skip_updates=True)


async def send_message(message: types.Message, bot: Bot):
    """Данная функция принимает сообщение пользователя и подбирает соответствующий Intent в качестве ответа"""
    try:
        session_id = str(message.from_user.id)
        response_text = detect_intent_texts(os.environ.get('PROJECT_ID'), session_id, message.text, 'ru')
        await bot.send_message(chat_id=session_id, text=response_text)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка: {str(e)}")


# Start the bot
if __name__ == '__main__':
    load_dotenv(find_dotenv())
    start()
