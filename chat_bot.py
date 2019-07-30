import urllib
from petrovich.main import Petrovich
from petrovich.enums import Case
import json
import urllib.request
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import cv2
import numpy
import logging
import sqlite3
import os


TOKEN = "08275b5e7122103670cb8da5d73e5287b968f93cfc7101233993f1516bef6cc6279445bba32d1f9e1a96c"

VK = vk_api.VkApi(token=TOKEN)

LONGPOLL = VkLongPoll(VK)

logging.basicConfig(filename="bot.log", level=logging.INFO)
logger = logging.getLogger("logger")

p = os.path.abspath('database')
conn = sqlite3.connect(p)
cursor = conn.cursor()

composite_req_dict = {}

empty_keyboad = json.dumps({"buttons":[],"one_time":True})

regular_keyboard=json.dumps({
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

admin_keyboard_1lvl=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Обновить замены"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Замены"
                                },
                                "color": "primary"
                            }]
                            ]},ensure_ascii=False)

admin_keyboard_2lvl=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Обновить замены"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Замены"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Добавить админа"
                                },
                                "color": "positive"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Разжаловать админа"
                                },
                                "color": "negative"
                            }]
                            ]},ensure_ascii=False)
authorities=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Обновлять замены"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Обновлять замены, управлять админами"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

menu_button=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

yes_or_no_keyboard=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Да"
                                },
                                "color": "positive"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Нет"
                                },
                                "color": "negative"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)



def write_msg(user_id, message,keyboard=regular_keyboard):
    '''
    Sends text message to user
    :param user_id:
    :param message:
    :return:
    '''
    VK.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(),
                                'message': message, 'keyboard':keyboard})

def get_admin_level(user_id):
    sql_req='SELECT * FROM admins WHERE user_id=?'
    cursor.execute(sql_req, [user_id])
    d = cursor.fetchone()
    if d:
        return d[1]
    else:
        return 0

def hub(user_id, message):
    lvl=get_admin_level(user_id)
    if lvl == 0:
        write_msg(user_id,message,regular_keyboard)
    elif lvl == 1:
        write_msg(user_id,message,admin_keyboard_1lvl)
    elif lvl >=2:
        write_msg(user_id, message, admin_keyboard_2lvl)


try:
    for event in LONGPOLL.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = VK.method('messages.getById', {'message_ids': event.message_id})
                request = event.text
                logger.log(logging.INFO,msg)

                if event.user_id in composite_req_dict.keys():
                    previous_req=composite_req_dict.pop(event.user_id)
                    if request == 'Главное меню':
                        hub(event.user_id,'Выход в главное меню')
                        continue
                    if previous_req['request_id'] == 'refresh_changes_1':
                        if (msg['items'][0]['attachments']):
                            if (msg['items'][0]['attachments'][0]['type'] == 'photo'):
                                photo_url = (msg['items'][0]['attachments'][0]['photo']['sizes'][4]['url'])
                                req = urllib.request.urlopen(photo_url)
                                arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
                                img = cv2.imdecode(arr, -1)
                                cv2.imwrite('schedule_changes.jpg', img)
                                hub(event.user_id, 'Замены успешно обновлены')
                            else:
                                hub(event.user_id, "Вы не прикрепили фото")
                        else:
                            hub(event.user_id, "Вы не прикрепили фото")

                    elif previous_req['request_id'] == 'add_admin_1':
                        try:
                            a = request.split('/')
                            composite_req_dict[event.user_id] = {'request_id': 'add_admin_2','data':str(VK.method('users.get',{'user_ids': a[3]})[0]['id'])}
                            write_msg(event.user_id,'Выберите полномочия нового админа',authorities)
                        except IndexError:
                            hub(event.user_id,'Неверная ссылка')
                        except sqlite3.IntegrityError:
                            hub(event.user_id, 'Пользователь уже админ')

                    elif previous_req['request_id'] == 'add_admin_2':
                        previous_req_data = previous_req['data']
                        user_info = VK.method('users.get', {'user_ids': previous_req_data})[0]
                        if request == 'Обновлять замены':
                            new_admin = previous_req_data, 1, str(user_info['first_name'] + ' ' + user_info['last_name'])
                        elif request == 'Обновлять замены, управлять админами':
                            new_admin = previous_req_data, 2, str(user_info['first_name'] + ' ' + user_info['last_name'])
                        else:
                            hub(event.user_id,'Неверная команда.')
                            continue
                        try:
                            if request == 'Обновлять замены':
                                write_msg(previous_req_data,
                                          'Теперь вы можете обновлять замены',
                                          admin_keyboard_1lvl)

                            elif request == 'Обновлять замены, управлять админами':
                                write_msg(previous_req_data,
                                          'Теперь вы можете обновлять замены, а так же назначать и разжаловать админов',
                                          admin_keyboard_2lvl)

                            cursor.execute("INSERT INTO admins(user_id,access_level,user_name) VALUES (?,?,?)", new_admin)
                            conn.commit()
                            hub(event.user_id,'Успешно')

                        except sqlite3.IntegrityError:
                            hub(event.user_id,'Пользователь уже админ')

                        except vk_api.exceptions.ApiError:
                            hub(event.user_id,'Пользователь не может быть назначен админом, так как еще не писал боту')

                    elif (previous_req['request_id']=='delete_admin_1'):
                        if request.isdigit():
                            if 1<=int(request)<=len(previous_req['data']):
                                petr = Petrovich()
                                name=previous_req['data'][int(request)-1][2].split()

                                persuaded_name = petr.firstname(name[0], Case.ACCUSATIVE) + ' ' + petr.lastname(name[1], Case.ACCUSATIVE)
                                msg = 'Вы уверены что хотите разжаловать ' + '[id'+str(previous_req['data'][int(request)-1][0])+'|'+persuaded_name+']?'
                                write_msg(event.user_id,msg,yes_or_no_keyboard)
                                composite_req_dict[event.user_id] = {'request_id': 'delete_admin_2', 'data':previous_req['data'][int(request)-1][0] }
                            else:
                                hub(event.user_id,'Неверный номер админа')
                        else:
                            hub(event.user_id,'Неверная команда')

                    elif (previous_req['request_id'] == 'delete_admin_2'):
                        if request=='Да':
                            if event.user_id !=  previous_req['data']:
                                if get_admin_level(event.user_id)>= get_admin_level(previous_req['data']):
                                    cursor.execute("DELETE FROM admins WHERE user_id=(?)",(previous_req['data'],))
                                    conn.commit()
                                    write_msg(previous_req['data'],'Вы больше не админ',regular_keyboard)
                                    hub(event.user_id,'Админ успешно разжалован')
                                else:
                                    hub(event.user_id,'Вы не можете разжаловать этого пользователя')
                            else:
                                hub(event.user_id,'Вы не можете разжаловать себя')
                        elif request == 'Нет':
                            hub(event.user_id,'Выход в главное меню')
                        else:
                            hub(event.user_id,'Неверная команда')


                elif request == "Замены":
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

                elif (request == "Обновить замены")and(get_admin_level(event.user_id)>0):
                    composite_req_dict[event.user_id]={'request_id': 'refresh_changes_1'}
                    write_msg(event.user_id,'Отправте фото',menu_button)

                elif request == 'Начать':
                    keyboard_json=regular_keyboard
                    greeting='Привет!\nЯ - ЧЧЧ-бот\nЯ умею присылать замены прямо в лс! Для этого, просто нажми кнопку \"Замены\"'
                    hub(event.user_id,greeting)

                elif request == 'clear':
                    write_msg(event.user_id,'Очищено',empty_keyboad)

                elif (request == 'Добавить админа')and(get_admin_level(event.user_id)>1):
                    composite_req_dict[event.user_id]={'request_id':'add_admin_1'}
                    write_msg(event.user_id,'Отправте ссылку на нового админа',menu_button)

                elif (request == 'Разжаловать админа')and(get_admin_level(event.user_id)>1):
                    cursor.execute("SELECT * FROM admins")
                    a=cursor.fetchall()
                    mes='Выберите админа, которого вы хотите разжаловать. Для этого отправте номер админа, указаный слева от его имени.\n\n'
                    for i in range(len(a)):
                        mes += str(i+1)+': ' + '[id'+str(a[i][0])+'|'+a[i][2]+']\n'
                    write_msg(event.user_id,mes,menu_button)
                    composite_req_dict[event.user_id] = {'request_id':'delete_admin_1','data':a}

                else:
                    hub(event.user_id, "Не понял вашего ответа...")

except Exception:
    logger.exception('Error')