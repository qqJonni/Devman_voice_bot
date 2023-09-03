from aiogram import Bot, Dispatcher, executor, types
from google.cloud import dialogflow
import os
from main import main
from detect_intent_texts import detect_intent_texts

main()

class Dispetcher:
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dp = Dispatcher(bot)


@Dispetcher.dp.message_handler()
async def start_command(message: types.Message):
    try:
        await detect_intent_texts('devmanvoicebot-ysve', str(message.from_user.id), message.text, 'ru')
        await Dispetcher.bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)
    except Exception as e:
        await Dispetcher.bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка : {str(e)}")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(Dispetcher.dp, skip_updates=True)

