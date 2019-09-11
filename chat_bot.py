import urllib
import keyboards
import time
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

token_file=open('token.txt')
TOKEN = token_file.read()
if '\n' in TOKEN:
    TOKEN = TOKEN[:-1]
token_file.close()

VK = vk_api.VkApi(token=TOKEN)

LONGPOLL = VkLongPoll(VK)

logging.basicConfig(filename="bot.log", level=logging.INFO)
logger = logging.getLogger("logger")

p = os.path.abspath('database')
conn = sqlite3.connect(p)
cursor = conn.cursor()

composite_req_dict = {}

def write_msg(user_id, message,keyboard=keyboards.regular_keyboard):
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

def get_main_menu_keyboard(user_id):
    lvl = get_admin_level(user_id)
    if lvl == 0:
        return keyboards.regular_keyboard
    elif lvl == 1:
        return keyboards.admin_keyboard_1lvl
    elif lvl >= 2:
        return keyboards.admin_keyboard_2lvl

def hub(user_id, message):
    lvl=get_admin_level(user_id)
    if lvl == 0:
        write_msg(user_id,message,keyboards.regular_keyboard)
    elif lvl == 1:
        write_msg(user_id,message,keyboards.admin_keyboard_1lvl)
    elif lvl >=2:
        write_msg(user_id, message, keyboards.admin_keyboard_2lvl)

logger.log(logging.INFO,'Start: '+time.ctime())

for event in LONGPOLL.listen():
    try:
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
                            write_msg(event.user_id,'Выберите полномочия нового админа',keyboards.authorities)
                        except IndexError:
                            hub(event.user_id,'Неверная ссылка')
                        except sqlite3.IntegrityError:
                            hub(event.user_id, 'Пользователь уже админ')
                        except vk_api.exceptions.ApiError:
                            hub(event.user_id, 'Неверная ссылка')

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
                            cursor.execute("INSERT INTO admins(user_id,access_level,user_name) VALUES (?,?,?)", new_admin)
                            if request == 'Обновлять замены':
                                write_msg(previous_req_data,
                                          'Теперь вы можете обновлять замены',
                                          keyboards.admin_keyboard_1lvl)

                            elif request == 'Обновлять замены, управлять админами':
                                write_msg(previous_req_data,
                                          'Теперь вы можете обновлять замены, а так же назначать и разжаловать админов',
                                          keyboards.admin_keyboard_2lvl)
                            conn.commit()
                            hub(event.user_id,'Успешно')

                        except sqlite3.IntegrityError:
                            hub(event.user_id,'Пользователь уже админ')

                        except vk_api.exceptions.ApiError:
                            hub(event.user_id,'Пользователь не может быть назначен админом, так как еще не писал боту')
                            cursor.execute("DELETE FROM admins WHERE user_id=(?)",
                                           (previous_req_data,))

                    elif (previous_req['request_id']=='delete_admin_1'):
                        if request.isdigit():
                            if 1<=int(request)<=len(previous_req['data']):
                                petr = Petrovich()
                                name=previous_req['data'][int(request)-1][2].split()

                                persuaded_name = petr.firstname(name[0], Case.ACCUSATIVE) + ' ' + petr.lastname(name[1], Case.ACCUSATIVE)
                                msg = 'Вы уверены что хотите разжаловать ' + '[id'+str(previous_req['data'][int(request)-1][0])+'|'+persuaded_name+']?'
                                write_msg(event.user_id,msg,keyboards.yes_or_no_keyboard)
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
                                    write_msg(previous_req['data'],'Вы больше не админ',keyboards.regular_keyboard)
                                    hub(event.user_id,'Админ успешно разжалован')
                                else:
                                    hub(event.user_id,'Вы не можете разжаловать этого пользователя')
                            else:
                                hub(event.user_id,'Вы не можете разжаловать себя')
                        elif request == 'Нет':
                            hub(event.user_id,'Выход в главное меню')
                        else:
                            hub(event.user_id,'Неверная команда')

                    elif previous_req['request_id'] == 'calendar':
                        correct_season=1
                        if request ==  'Осень':
                            image_name='calendar_fall.jpg'
                        elif request == 'Зима':
                            image_name = 'calendar_winter.jpg'
                        elif request == 'Весна':
                            image_name = 'calendar_spring.jpg'
                        elif request == 'Лето':
                            image_name = 'calendar_summer.jpg'
                        else:
                            hub(event.user_id,'Неверная команда')
                            correct_season=0
                        if correct_season:
                            upload_url = VK.method('photos.getMessagesUploadServer')
                            photo_to_upload = open('calendar/'+image_name, 'rb')
                            response = requests.post(upload_url['upload_url'],
                                                     files={'photo': photo_to_upload}).json()
                            saved_photo = VK.method('photos.saveMessagesPhoto',
                                                    {'photo': response['photo'], 'server': response['server'],
                                                     'hash': response['hash']})[0]
                            photo_info = 'photo{}_{}'.format(saved_photo['owner_id'], saved_photo['id'])
                            VK.method('messages.send', {'user_id': event.user_id, 'random_id': get_random_id(),
                                                        'attachment': photo_info,'keyboard':get_main_menu_keyboard(event.user_id)})

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
                                                'attachment': photo_info,'keyboard':get_main_menu_keyboard(event.user_id)})

                elif (request == "Обновить замены")and(get_admin_level(event.user_id)>0):
                    composite_req_dict[event.user_id]={'request_id': 'refresh_changes_1'}
                    write_msg(event.user_id,'Отправте фото',keyboards.menu_button)

                elif request == 'Начать':
                    keyboard_json=keyboards.regular_keyboard
                    greeting='Привет!\nЯ - ЧЧЧ-бот\nЯ умею присылать замены прямо в лс! Для этого, просто нажми кнопку \"Замены\"'
                    hub(event.user_id,greeting)

                elif request == 'clear':
                    write_msg(event.user_id,'Очищено',keyboards.empty_keyboad)

                elif (request == 'Добавить админа')and(get_admin_level(event.user_id)>1):
                    composite_req_dict[event.user_id]={'request_id':'add_admin_1'}
                    write_msg(event.user_id,'Отправте ссылку на нового админа',keyboards.menu_button)

                elif (request == 'Разжаловать админа')and(get_admin_level(event.user_id)>1):
                    cursor.execute("SELECT * FROM admins")
                    a=cursor.fetchall()
                    mes='Выберите админа, которого вы хотите разжаловать. Для этого отправте номер админа, указаный слева от его имени.\n\n'
                    for i in range(len(a)):
                        mes += str(i+1)+': ' + '[id'+str(a[i][0])+'|'+a[i][2]+']\n'
                    write_msg(event.user_id,mes,keyboards.menu_button)
                    composite_req_dict[event.user_id] = {'request_id':'delete_admin_1','data':a}

                elif request  == 'Календарь учебного года':
                    write_msg(event.user_id, 'Выбери время года', keyboards.seasons)
                    composite_req_dict[event.user_id] = {'request_id': 'calendar'}

                else:
                    hub(event.user_id, "Не понял вашего ответа...")

    except Exception:
        logger.exception('Error')
logger.log(logging.INFO,'Finish: '+time.ctime())