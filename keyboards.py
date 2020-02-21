import json

empty_keyboad = json.dumps({"buttons":[],"one_time":True})

regular_keyboard_pos_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Подписка на замены"
                                },
                                "color": "positive"
                            }]
                            ]},ensure_ascii=False)

regular_keyboard_neg_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Подписка на замены"
                                },
                                "color": "negative"
                            }]
                            ]},ensure_ascii=False)

admin_keyboard_1lvl_pos_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
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
                                "label": "Подписка на замены"
                                },
                                "color": "positive"
                            }]
                            ]},ensure_ascii=False)

admin_keyboard_1lvl_neg_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
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
                                "label": "Подписка на замены"
                                },
                                "color": "negative"
                            }]
                            ]},ensure_ascii=False)

admin_keyboard_2lvl_pos_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
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
                                "label": "Подписка на замены"
                                },
                                "color": "positive"
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

admin_keyboard_2lvl_neg_ch=json.dumps({
                            "one_time": False,
                            "buttons": [
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
                                "label": "Календарь учебного года"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Расписание уроков"
                                },
                                "color": "primary"
                            }],
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
                                "label": "Подписка на замены"
                                },
                                "color": "negative"
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

seasons=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Осень"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Зима"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Весна"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Лето"
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

parallels=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "5"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "7"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "9"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "10"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "11"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Сообщить об ошибке в расписании"
                                },
                                "color": "negative"
                            }]
                            ]},ensure_ascii=False)

parallel_5=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "5А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5В\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5Г\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "5М",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5М\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5Н",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5Н\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5ТЛ",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5ТЛ\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "5Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"5Э\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_6=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "6А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6В\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6Г\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "6М",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6М\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6Н",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6Н\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6ТЛ",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6ТЛ\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "6Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"6Э\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_7=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "7А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "7Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "7М",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7М\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "7Н",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7Н\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "7О",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7О\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "7ТЛ",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7ТЛ\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "7Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"7Э\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_8=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "8А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8В\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8Г\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "8М",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8М\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8Н",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8Н\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "8Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"8Э\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_9=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "9А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"9А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "9Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"9Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "9В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"9В\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "9Н",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"9Н\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "9Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"9Э\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_10=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "10А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"10А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "10Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"10Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "10В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"10В\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "10Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"10Г\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "10Д",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"10Д\"}"
                                },
                                "color": "primary"
                            }
                            ],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

parallel_11=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "11А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11В\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "11Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Г\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Д",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Д\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Э\"}"
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

parallel_11=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "11А",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11А\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Б",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Б\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11В",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11В\"}"
                                },
                                "color": "primary"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "11Г",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Г\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Д",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Д\"}"
                                },
                                "color": "primary"
                            },
                            {
                                "action": {
                                "type": "text",
                                "label": "11Э",
                                "payload": "{\"command\": \"timetable_2\",\"button\": \"11Э\"}"
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

enable_subscription=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Подписаться на обновления замен"
                                },
                                "color": "positive"
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Главное меню"
                                },
                                "color": "secondary"
                            }]
                            ]},ensure_ascii=False)

disable_subscription=json.dumps({
                            "one_time": False,
                            "buttons": [
                            [{
                                "action": {
                                "type": "text",
                                "label": "Отписаться от обновлений замен"
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