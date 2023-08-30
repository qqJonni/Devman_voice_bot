import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow
import os
from dotenv import load_dotenv, find_dotenv


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback is True:
        pass
    else:

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
                response.query_result.intent.is_fallback
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.intent))

        vk_api.messages.send(user_id=event.user_id, message=response.query_result.fulfillment_text, random_id=random.randint(1,1000))


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    vk_session = vk.VkApi(token=os.environ.get('TOKEN_VK'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts('devmanvoicebot-ysve', 'new', event.text, 'ru')

