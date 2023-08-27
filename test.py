from aiogram import Bot, Dispatcher, executor, types
from google.cloud import dialogflow
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


# Define the handler for the "/start" command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Call the detect_intent_texts function and pass the necessary parameters
    await detect_intent_texts('devmanvoicebot-ysve', str(message.from_user.id), message.text, 'ru')


# Define the detect_intent_texts function
async def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the intent detection result with text input.
    Using the same `session_id` between requests allows continuation of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    # Send the fulfillment text back to the user on Telegram
    await bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)