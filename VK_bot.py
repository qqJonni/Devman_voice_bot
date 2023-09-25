import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv

from detect_intent_texts import detect_intent_texts


def start():
    load_dotenv(find_dotenv())
    """Данная функция принимает сообщение пользователя и подбирает соответствующий Intent в качестве ответа"""
    vk_session = vk.VkApi(token=os.environ.get('TOKEN_VK'))
    vk_api = vk_session.get_api()
    for event in VkLongPoll(vk_session).listen():
        session_id = str(event.peer_id)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = detect_intent_texts(os.environ.get('PROJECT_ID'), session_id, event.text, 'ru')
            if not response.query_result.intent.is_fallback:
                text = response.query_result.fulfillment_text
                print(text)
                vk_api.messages.send(user_id=event.user_id, message=text, random_id=random.randint(1, 1000))


if __name__ == "__main__":
    start()
