import urllib
import json
import urllib.request
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import cv2
import numpy
import logging


def write_msg(user_id, message):
    '''
    Sends text message to user
    :param user_id:
    :param message:
    :return:
    '''
    VK.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(),
                                'message': message})

TOKEN = "08275b5e7122103670cb8da5d73e5287b968f93cfc7101233993f1516bef6cc6279445bba32d1f9e1a96c"

VK = vk_api.VkApi(token=TOKEN)

LONGPOLL = VkLongPoll(VK)

logging.basicConfig(filename="bot.log", level=logging.INFO)
logger = logging.getLogger("logger")

try:
    for event in LONGPOLL.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = VK.method('messages.getById', {'message_ids': event.message_id})
                request = event.text
                logger.log(logging.INFO,msg)

                if request == "Замены":
                    upload_url = VK.method('photos.getMessagesUploadServer')
                    photo_to_upload = open('schedule_changes.jpg', 'rb')
                    response = requests.post(upload_url['upload_url'],
                                             files={'photo':photo_to_upload}).json()
                    saved_photo = VK.method('photos.saveMessagesPhoto',
                                            {'photo': response['photo'], 'server':response['server'],
                                             'hash': response['hash']})[0]
                    photo_info = 'photo{}_{}'.format(saved_photo['owner_id'], saved_photo['id'])
                    VK.method('messages.send', {'user_id': event.user_id, 'random_id': get_random_id(),
                                                'attachment': photo_info})

                elif request == "А":
                    write_msg(event.user_id, "Всё хорошо")

                elif (request == "Обновить")and(event.user_id == 271296808):
                    if(msg['items'][0]['attachments']):
                        if(msg['items'][0]['attachments'][0]['type']=='photo'):
                            photo_url = (msg['items'][0]['attachments'][0]['photo']['sizes'][4]['url'])
                            req = urllib.request.urlopen(photo_url)
                            arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
                            img = cv2.imdecode(arr, -1)
                            cv2.imwrite('schedule_changes.jpg', img)
                            write_msg(event.user_id, 'Замены успешно обновлены')
                        else:
                            write_msg(event.user_id, "Вы не прикрепили фото")
                    else:
                        write_msg(event.user_id, "Вы не прикрепили фото")

                elif request == 'Начать':
                    keyboard_json=json.dumps({
                                  "one_time": False,
                                  "buttons": [
                                    [{
                                      "action": {
                                        "type": "text",
                                        "label": "Замены"
                                      },
                                      "color": "primary"
                                    }]
                                  ]},ensure_ascii=False)
                    greeting='Привет!\nЯ - ЧЧЧ-бот\nЯ умею присылать замены прямо в лс! Для этого, просто нажми кнопку \"Замены\"'
                    VK.method('messages.send', {'user_id': event.user_id, 'random_id': get_random_id(),'keyboard': keyboard_json,'message':greeting})

                elif request == 'clear':
                    keyboard_json = json.dumps({"buttons":[],"one_time":True})
                    VK.method('messages.send',
                              {'user_id': event.user_id, 'random_id': get_random_id(), 'keyboard': keyboard_json ,
                               'message': 'Очищено'})
                else:
                    write_msg(event.user_id, "Не понял вашего ответа...")
except Exception:
    logger.exception('Error')