from aiogram import Bot, Dispatcher, executor, types
from google.cloud import dialogflow
import os
from main import main

main()

class Dispetcher:
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dp = Dispatcher(bot)


@Dispetcher.dp.message_handler()
async def start_command(message: types.Message):
    # Call the detect_intent_texts function and pass the necessary parameters
    try:
        await detect_intent_texts('devmanvoicebot-ysve', str(message.from_user.id), message.text, 'ru')
    except Exception as e:
        await Dispetcher.bot.send_message(chat_id=message.chat.id, text=f"Произошла ошибка : {str(e)}")


# Define the detect_intent_texts function
async def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the intent detection result with text input.
    Using the same `session_id` between requests allows continuation of the conversation."""
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        await Dispetcher.bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)
    except Exception as e:
        await Dispetcher.bot.send_message(chat_id=session_id, text=f"Произошла ошибка: {str(e)}")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(Dispetcher.dp, skip_updates=True)

