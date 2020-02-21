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




p = os.path.abspath('database')
conn = sqlite3.connect(p)
cursor = conn.cursor()

composite_req_dict = {}

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO,filemode='a'):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file,filemode)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def write_msg(user_id, message,keyboard=keyboards.regular_keyboard_neg_ch):
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
    cursor.execute("SELECT sub_id FROM subscribers WHERE sub_id=(?)", (user_id,))
    if cursor.fetchone()==None:
        sub_keyboard=0
    else:
        sub_keyboard = 1
    if sub_keyboard:
        if lvl == 0:
            return keyboards.regular_keyboard_pos_ch
        elif lvl == 1:
            return keyboards.admin_keyboard_1lvl_pos_ch
        elif lvl >= 2:
            return keyboards.admin_keyboard_2lvl_pos_ch
    else:
        if lvl == 0:
            return keyboards.regular_keyboard_neg_ch
        elif lvl == 1:
            return keyboards.admin_keyboard_1lvl_neg_ch
        elif lvl >= 2:
            return keyboards.admin_keyboard_2lvl_neg_ch

def hub(user_id, message):
    write_msg(user_id,message,get_main_menu_keyboard(user_id))

logger = setup_logger('info_and_error_logger', 'bot.log')
msg_logger = setup_logger('messages_logger', 'msgs.log')
time_logger=setup_logger('time_logger','time.log')

logger.info('Start')
f = open('stat.txt', 'r')
try: #TODO адекватная реация на отсутствие файла
    current_day = int(f.read().split()[-6].split('.')[0])+1
except IndexError:
    f.close()
    f=open('stat.txt', 'w')
    f.write(str('//////////////////////////////////////////////////\nINITIAL '+ time.strftime('%d.%m.%Y',time.localtime(time.time()-86400))+': '+'0'+'\nЗа всё время: '+'0'+'\n'))
    current_day=0
f.close()
for event in LONGPOLL.listen():

    try:
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                exec_start=time.process_time()

                if current_day != int(time.strftime('%d')):
                    f = open('stat.txt', 'r+') #TODO Обнулить счётчик перед релизом
                    total_mes=int(f.read().split()[-1])

                    temp_f = open('today_stat.txt', 'r+')
                    try:
                        mes_counter = int(temp_f.read())
                    except ValueError:
                        mes_counter=0
                    temp_f.seek(0)
                    temp_f.write('1')
                    temp_f.truncate()
                    temp_f.close()
                    report=str('//////////////////////////////////////////////////\nСтатистика за '+ time.strftime('%d.%m.%Y',time.localtime(time.time()-86400))+': '+str(mes_counter)+'\nЗа всё время: '+str(total_mes+mes_counter)+'\n')
                    f.write(report)
                    f.close()
                    current_day = int(time.strftime('%d'))
                else:
                    f = open('today_stat.txt', 'r+')
                    mes_counter = int(f.read())
                    f.seek(0)
                    f.write(str(mes_counter + 1))
                    f.truncate()
                    f.close()
                msg = VK.method('messages.getById', {'message_ids': event.message_id})
                request = event.text
                msg_logger.info(msg)
                if 'payload' in msg['items'][0]:
                    payload=json.loads(msg['items'][0]['payload'])
                    if payload['command']=='start':
                        keyboard_json = get_main_menu_keyboard(event.user_id)
                        greeting = 'Привет!\nЯ - ЧЧЧ-бот\nЯ умею присылать замены и расписание прямо в лс! Для этого, просто нажми кнопку нужной тебе функции'
                        hub(event.user_id, greeting)

                    elif payload['command']=='timetable_2':
                        try:
                            if payload['button'][1].isdigit():
                                form = request[:2]
                                form_letter = payload['button'][2:len(payload['button'])]
                            else:
                                form = request[:1]
                                form_letter = payload['button'][1:len(payload['button'])]
                            timetable = open('timetables/' + form + '/' + form+form_letter + '.txt', 'r').read()
                            hub(event.user_id, timetable)
                        except FileNotFoundError:
                            hub(event.user_id, 'Класс не сущесвует или еще не добавлен')
                    else:
                        hub(event.user_id, 'Неверная команда')

                else:
                    if event.user_id in composite_req_dict.keys():
                        previous_req=composite_req_dict.pop(event.user_id)
                        if request == 'Главное меню':
                            hub(event.user_id,'Выход в главное меню')
                            continue
                        if previous_req['request_id'] == 'refresh_changes_1':
                            if (msg['items'][0]['attachments']):
                                if (msg['items'][0]['attachments'][0]['type'] == 'photo'):
                                    sizes_dict=msg['items'][0]['attachments'][0]['photo']['sizes']
                                    max_size=0
                                    max_size_id=0
                                    for i in range(len(sizes_dict)):
                                        curr_size=sizes_dict[i]['width']*sizes_dict[i]['height']
                                        if curr_size>max_size:
                                            max_size = curr_size
                                            max_size_id = i
                                    photo_url = (msg['items'][0]['attachments'][0]['photo']['sizes'][max_size_id]['url'])
                                    req = urllib.request.urlopen(photo_url)
                                    arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
                                    img = cv2.imdecode(arr, -1)
                                    cv2.imwrite('schedule_changes_temp.jpg', img)
                                    upload_url = VK.method('photos.getMessagesUploadServer')
                                    photo_to_upload = open('schedule_changes_temp.jpg', 'rb')
                                    response = requests.post(upload_url['upload_url'],
                                                             files={'photo': photo_to_upload}).json()
                                    saved_photo = VK.method('photos.saveMessagesPhoto',
                                                            {'photo': response['photo'], 'server': response['server'],
                                                             'hash': response['hash']})[0]
                                    photo_info = 'photo{}_{}'.format(saved_photo['owner_id'], saved_photo['id'])
                                    VK.method('messages.send', {'user_id': event.user_id, 'random_id': get_random_id(),
                                                                'attachment': photo_info, 'message': 'Обновить замены данной картинкой?',
                                                                'keyboard': keyboards.yes_or_no_keyboard})
                                    composite_req_dict[event.user_id] = {'request_id': 'refresh_changes_2'}

                                else:
                                    hub(event.user_id, "Вы не прикрепили фото")
                            else:
                                hub(event.user_id, "Вы не прикрепили фото")

                        elif previous_req['request_id'] == 'refresh_changes_2':
                            if request=='Да':
                                os.remove('schedule_changes.jpg')
                                os.rename('schedule_changes_temp.jpg','schedule_changes.jpg')
                                hub(event.user_id,'Замены успешно обновлены')
                                cursor.execute("SELECT sub_id FROM subscribers")
                                subs=cursor.fetchall()
                                upload_url = VK.method('photos.getMessagesUploadServer')
                                photo_to_upload = open('schedule_changes.jpg', 'rb')
                                response = requests.post(upload_url['upload_url'],
                                                         files={'photo': photo_to_upload}).json()
                                saved_photo = VK.method('photos.saveMessagesPhoto',
                                                        {'photo': response['photo'], 'server': response['server'],
                                                         'hash': response['hash']})[0]
                                photo_info = 'photo{}_{}'.format(saved_photo['owner_id'], saved_photo['id'])
                                for i in subs:
                                    try:
                                        VK.method('messages.send', {'user_id': i[0], 'random_id': get_random_id(),
                                                                    'attachment': photo_info,
                                                                    'message': 'Лови свежие замены',
                                                                    'keyboard': get_main_menu_keyboard(i[0])})
                                    except Exception:
                                        logger.exception('Error')
                            else:
                                os.remove('schedule_changes_temp.jpg')
                                hub(event.user_id, 'Отмена')

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
                                              get_main_menu_keyboard(event.user_id))

                                elif request == 'Обновлять замены, управлять админами':
                                    write_msg(previous_req_data,
                                              'Теперь вы можете обновлять замены, а так же назначать и разжаловать админов',
                                              get_main_menu_keyboard(event.user_id))
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
                                        write_msg(previous_req['data'],'Вы больше не админ',get_main_menu_keyboard(event.user_id))
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

                        elif previous_req['request_id']=='timetable_1':
                            if request.isdigit() and len(request)<=2:
                                try:
                                    if request=='5':
                                        form_keyboard=keyboards.parallel_5
                                    elif request == '6':
                                        form_keyboard = keyboards.parallel_6
                                    elif request == '7':
                                        form_keyboard = keyboards.parallel_7
                                    elif request == '8':
                                        form_keyboard = keyboards.parallel_8
                                    elif request == '9':
                                        form_keyboard = keyboards.parallel_9
                                    elif request == '10':
                                        form_keyboard = keyboards.parallel_10
                                    elif request == '11':
                                        form_keyboard = keyboards.parallel_11
                                    write_msg(event.user_id, 'Выбери класс', form_keyboard)
                                except AttributeError:
                                    hub(event.user_id,'Параллель не существует или еще не добавлена')
                            elif request =='Сообщить об ошибке в расписании':
                                write_msg(event.user_id,'Опиши ошибку: в расписании какого класса, в какой день, в каких '
                                'уроках она содержится, и в чем она состоит. Наши администраторы постараются '
                                'исправить ее как можно скорее.',keyboards.menu_button)
                                composite_req_dict[event.user_id] = {'request_id': 'TimetableError'}
                            else:
                                hub(event.user_id,' Неверная команда')

                        elif previous_req['request_id'] == 'TimetableError':
                            hub(event.user_id,'Большое спасибо за внимательность. Скоро все будет исправлено.')
                            cursor.execute("SELECT * FROM admins")
                            a = cursor.fetchall()
                            max_admin_level,max_admin_level_id=0,0
                            for i in range(len(a)):
                                if a[i][1] > max_admin_level:
                                    max_admin_level=a[i][1]
                                    max_admin_level_id=a[i][0]
                            VK.method('messages.send', {'user_id': str(max_admin_level_id), 'random_id': get_random_id(),
                                                        'message': 'В расписании ошибка, разберись', 'forward_messages':event.message_id})

                        elif previous_req['request_id']=='user_sub_1':
                            if request=='Подписаться на обновления замен':
                                cursor.execute("INSERT INTO subscribers(sub_id) VALUES (?)", (event.user_id,))
                                hub(event.user_id,'Теперь ты подписан на обновления замен')

                            elif request=='Отписаться от обновлений замен':
                                cursor.execute("DELETE FROM subscribers WHERE sub_id=(?)", (event.user_id,))
                                hub(event.user_id,'Подписка на обновления замен отменена')


                            else:
                                hub(event.user_id,'Неверная команда')
                            conn.commit()


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
                        write_msg(event.user_id,'Отправьте фото',keyboards.menu_button)

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

                    elif request  == 'Расписание уроков':
                        write_msg(event.user_id,'Выбери параллель',keyboards.parallels)
                        composite_req_dict[event.user_id] = {'request_id': 'timetable_1'}

                    elif request  == 'Подписка на замены' or request=='Ы':
                        cursor.execute("SELECT sub_id FROM subscribers WHERE sub_id=(?)", (event.user_id,))
                        sub_status=cursor.fetchone()
                        if sub_status==None:
                            write_msg(event.user_id, 'Подписка не активна', keyboards.enable_subscription)
                        else:
                            write_msg(event.user_id, 'Подписка активна', keyboards.disable_subscription)
                        composite_req_dict[event.user_id] = {'request_id': 'user_sub_1'}

                    else:
                        if (VK.method('messages.getHistory', {'user_id': event.user_id})['count']==1):
                            hub(event.user_id, "Здравствуйте!\nЭто сообщение отправлено автоматически нашим замечательным "
                            "ботом, и админы группы могут его пропустить.\nЕсли вы хотите предложить новость "
                            "для публикации, вы можете сделать это на главной странице группы, воспользовавшись "
                            "функцией \"Предложить новость\".\nТам же вы можете найти контакты админов, с которыми " 
                            "можно связаться, если у вас остались вопросы.")
                        else:
                            hub(event.user_id, "Мой искусственный интеллект не знает, что на это ответить😔️")

                    exec_stop=time.process_time()
                    time_logger.info('Command: '+event.text+'. Duration: '+str(exec_stop-exec_start))
    except Exception:
        logger.exception('Error')
logger.info('Finish')
