import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from detect_intent_texts import detect_intent_texts
from main import main


if __name__ == "__main__":
    main()
    vk_session = vk.VkApi(token=os.environ.get('TOKEN_VK'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts('devmanvoicebot-ysve', 'new', event.text, 'ru')
            if response.query_result.intent.is_fallback is False:
                vk_api.messages.send(user_id=event.user_id, message=response.query_result.fulfillment_text,
                                     random_id=random.randint(1, 1000))

