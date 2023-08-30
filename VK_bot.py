import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow
import os
from dotenv import load_dotenv, find_dotenv


async def detect_intent_texts(project_id, session_id, text, language_code):

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
    print("Fulfillment text: {}\n".format(response.query_result.intent))

    # Send the fulfillment text back to the user on Telegram
    await bot.send_message(chat_id=session_id, text=response.query_result.fulfillment_text)

load_dotenv(find_dotenv())
vk_session = vk.VkApi(token=os.environ.get('TOKEN_VK'))
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            detect_intent_texts('devmanvoicebot-ysve', str(message.from_user.id), message.text, 'ru')

