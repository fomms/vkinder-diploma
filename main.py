from VKbot import VKbot
from vk_api.longpoll import VkEventType
from vk_api_my import VKAPIusers
from db.db_in_get_info import *
from tokens import access_token, group_token
import time


vkbot = VKbot(group_token)  # создаем экземляр класса

vkbot.get_started()  # пускаем первый лонгпол который получает айди
min_age, max_age = vkbot.get_info()  # получаем границы возраста
city = vkbot.get_city()  # получаем город

vkapi = VKAPIusers(min_age, max_age, city, sex=1)  # создаем экземляр класса пользователей приложения для примененния к ним методов поиска
# print(vkapi.search_users())
# id_user = vkbot.user_id

search_users = vkapi.search_users() # вызов метода поиска к пользовательлю 1


parse_users_vk_list(search_users, vkbot.user_id)  # вызов функции наполнения БД текущего юзера
add_new(search_users, vkbot.user_id)  # довавляем найденных кандидатов для предложения юзеру в БД

pair = get_searh_pair_info(session, vkbot.user_id)  # извекаем кандидатов для предложения юзеру, возвращает объект итератор

def iterator(it):
    '''функция которая помогает итерироваться по списку кандидатов'''
    try:
        selected = next(it)  # помещает сюда текущего кандидата
        print(selected)
        vkbot.send_candidate(selected)
        return selected  # возвращаем текущего кандидата для возможности заненсения его в иззбранное
    except StopIteration:
        print('end Анкеты кончились')
        return False


last_one = True
print('GO')
vkbot.send_message(vkbot.user_id, message='Можете начинать, нажав кнопку NEXT')
for event in vkbot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text
        # if last_one is False:    # по задумке в этом блоке мы получаем новую порцию кандидатов с выбранным offset
            #  vkapi.offset += 10  # но это не работает, итератор не обновляется(((
            #  search_users = vkapi.search_users()
            #  print(search_users)
            #  add_new(search_users, vkbot.user_id)
            #  pair = get_new_searh_pair_info(session, vkbot.user_id)
            #  pair, last_one = renew_iter(pair)

        if msg == 'NEXT':  # показать кандидата
            last_one = iterator(pair)
            if last_one is not False:
                update_db_attribute(session, vkbot.user_id, last_one[2][17:], 3)  # пометить кандидата как просмотренного

        elif msg == 'ADD_TO_FAVOURITE':  # меняем в последнем кандидате параметр FAVOURITE

            vkbot.send_message(event.user_id, message='Анкета добавлена в избранное!')
            if last_one is not False:
                update_db_attribute(session, vkbot.user_id, last_one[2][17:], 1)  # пометить кандидата как просмотренного
            else:
                vkbot.send_message(event.user_id, message='Вы еще никокого не посмотрели')

        elif msg == 'ADD_TO_BLACK_LIST':  # меняем в последнем кандидате параметр BLACK_LIST

            vkbot.send_message(event.user_id, message='Анкета добавлена в заблокированное!')
            if last_one is not False:
                update_db_attribute(session, vkbot.user_id, last_one[2][17:], 2)  # пометить кандидата как заблокированного
            else:
                vkbot.send_message(event.user_id, message='Вы еще никокого не посмотрели')

        elif msg == 'SHOW_FAVOURITE':  # показаваем человеку всех в избранном

            for liked in get_list_likes_pair(session, vkbot.user_id):
                vkbot.send_candidate(liked)
                time.sleep(0.5)

        elif msg == 'SHOW_BLACK_LIST':  # показаваем человеку всех в заблокированном

            for blocked in get_list_blocked_pair(session, vkbot.user_id):
                vkbot.send_candidate(blocked)
                time.sleep(0.5)

        else:
            vkbot.send_message(event.user_id, message='Чтобы начать напишите боту "старт')


session.close()