import json

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
                            }],
                            [{
                                "action": {
                                "type": "text",
                                "label": "Календарь учебного года"
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
                                "label": "Обновить замены"
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
                                "label": "Обновить замены"
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

