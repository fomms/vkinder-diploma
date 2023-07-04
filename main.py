from VKbot import VKbot
from vk_api.longpoll import VkEventType
from vk_api_my import VKAPIusers
from db.db_in_get_info import *
from tokens import access_token, group_token


vkbot = VKbot(group_token)

vkbot.get_started()
min_age, max_age = vkbot.get_info()
city = vkbot.get_city()

vkapi = VKAPIusers(min_age, max_age, city, sex=1)   #экземпляры класса пользователей приложения для примененния к ним методов поиска
print(vkapi.search_users())
id_user = vkbot.user_id

search_users = vkapi.search_users() #вызов метода поиска к пользовательлю 1


parse_users_vk_list(search_users, id_user) #вызов функции наполнения БД для какого то из поисков
add_new(search_users, id_user)

pair = get_searh_pair_info(session, id_user)

def iterator(it):

        try:
            selected = next(it)
            print(selected)
            vkbot.send_message(event.user_id, message=f'{selected[0]} {selected[1]} /n {selected[2]} /n ', attachment=selected[3])
            return selected
        except StopIteration:
            print('end')
            return False


last_one = True
#
#
for event in vkbot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text
        if last_one is False:
            vkapi.offset += 10
            search_users = vkapi.search_users()
            print(search_users)
            add_new(search_users, id_user)
            pair = get_new_searh_pair_info(session, id_user)

        if msg == 'NEXT':
            # pair = get_searh_pair_info(session, 1)
            print(type(pair))
            last_one = iterator(pair)
            print(last_one)
            if last_one is not False:
                update_db_attribute(session, id_user, last_one[2][17:], 3) # пометить кандидата как просмотренного

        elif msg == 'ADD_TO_FAVOURITE':
            """меняем в последнем кандидате параметр FAVOURITE"""
            vkbot.send_message(event.user_id, message='Анкета добавлена в избранное!')

        elif msg == 'ADD_TO_BLACK_LIST':
            """меняем в последнем кандидате параметр BLACK_LIST"""
            vkbot.send_message(event.user_id, message='Анкета добавлена в заблокированное!')

        elif msg == 'SHOW_FAVOURITE':
            """показаваем человеку всех в избранном"""

        elif msg == 'SHOW_BLACK_LIST':
            """показаваем человеку всех в заблокированном"""


session.close()