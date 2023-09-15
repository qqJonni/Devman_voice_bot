import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv

from detect_intent_texts import detect_intent_texts


def start():
    """Данная функция принимает сообщение пользователя и подбирает соответствующий Intent в качестве ответа"""
    vk_session = vk.VkApi(token=os.environ.get('TOKEN_VK'))
    vk_api = vk_session.get_api()
    for event in VkLongPoll(vk_session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = detect_intent_texts(os.environ.get('PROJECT_ID'), f'{vk_session}', event.text, 'ru')
            if response.query_result.intent.is_fallback:
                pass
            try:
                vk_api.messages.send(user_id=event.user_id, message=response, random_id=random.randint(1, 1000))
            except Exception as e:
                vk_api.messages.send(user_id=event.user_id, message=f"Произошла ошибка: {str(e)}", random_id=0)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    start()
