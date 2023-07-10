from vk_api.longpoll import VkEventType
from db.db_in_get_info import *
from tokens import group_token
from iterator import PeopleIterator
from VKbot import VKbot
import time

if __name__ == '__main__':
    vkbot = VKbot(group_token)
    main_flag = True

    for event in vkbot.longpoll.listen():

        while main_flag is True:
            vkbot.get_started()  # пускаем первый лонгпол который получает айди
            vkapi = VKAPIusers(vkbot.get_min_age(), vkbot.get_max_age(), city=vkbot.get_city(),
                               sex=vkbot.get_sex())  # создаем экземляр класса пользователей приложения для примененния к ним методов поиска
            search_users = vkapi.search_users()  # вызов метода поиска к пользовательлю 1
            if check_user(session, vkbot.user_id) is None:
                print(check_user(session, vkbot.user_id))
                add_user(vkbot.user_id)  # вызов функции наполнения БД текущего юзера
            add_new(search_users, vkbot.user_id)  # довавляем найденных кандидатов для предложения юзеру в БД
            pair = get_new_searh_pair_info(session,
                                       vkbot.user_id)  # извекаем кандидатов для предложения юзеру, возвращает объект итератор
            i = PeopleIterator(pair)  # Создаём первичный экземпляр иторатора
            iter(i)
            last_one = False
            main_flag = False
            vkbot.send_message(message='Можете начинать, нажав кнопку NEXT')
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            msg = event.text
            if msg == 'NEXT':  # показать кандидата

                try:  # Блок для корректной работы кнопки НЕКСТ
                    if i.flag is False:
                        i = PeopleIterator(new_pair)
                        iter(i)
                    last_one = next(i)
                    print(last_one)
                    vkbot.send_candidate(last_one)  # метод выводит анкеты по одной
                    update_db_attribute(session, vkbot.user_id, last_one[2][17:], 3)  # помечает последнюю анкету как просмотренную
                except StopIteration:
                    vkbot.send_message(message='Поиск дополнительных анкет.....')
                    vkapi.offset += 3  # необходимо выставлять значение равное количетсву первично найденных людей
                    search_users = vkapi.search_users()  # ищет новых людей с указанным отступом
                    if not search_users:
                        vkbot.send_message(message='Анкеты кончились, для изменения параметров поиска введите: старт', keyboard=vkbot.get_keyboard('dead_key.json'))
                        main_flag = True
                    else:
                        add_new(search_users, vkbot.user_id)  # добаляет новых людей в базу данных
                        new_pair = get_new_searh_pair_info(session, vkbot.user_id)  # извлекает непросмотренных людей из базы данных
                        # print(new_pair)                    vkbot.send_message(message='Можете продолжить, нажав кнопку NEXT')

            elif msg == 'ADD_TO_FAVOURITE':  # меняем в последнем кандидате параметр FAVOURITE

                if last_one is not False:
                    update_db_attribute(session, vkbot.user_id, last_one[2][17:], 1)  # пометить кандидата как просмотренного
                    vkbot.send_message(message='Анкета добавлена в избранное!')
                else:
                    vkbot.send_message(message='Вы еще никокого не посмотрели')

            elif msg == 'ADD_TO_BLACK_LIST':  # меняем в последнем кандидате параметр BLACK_LIST

                if last_one is not False:
                    update_db_attribute(session, vkbot.user_id, last_one[2][17:], 2)  # пометить кандидата как заблокированного
                    vkbot.send_message(message='Анкета добавлена в заблокированное!')
                else:
                    vkbot.send_message(message='Вы еще никокого не посмотрели')

            elif msg == 'SHOW_FAVOURITE':  # показаваем человеку всех в избранном
                liked_list = get_list_likes_pair(session, vkbot.user_id)
                if len(liked_list) == 0:
                    vkbot.send_message(message='Вы еще никого не добавили в избранное')
                else:
                    for liked in get_list_likes_pair(session, vkbot.user_id):
                        vkbot.send_candidate(liked)
                        time.sleep(0.5)

            elif msg == 'SHOW_BLACK_LIST':  # показаваем человеку всех в заблокированном
                block_list = get_list_blocked_pair(session, vkbot.user_id)
                if len(block_list) == 0:
                    vkbot.send_message(message='Вы еще никого не добавили в заблокированное')
                else:
                    for blocked in get_list_blocked_pair(session, vkbot.user_id):
                        vkbot.send_candidate(blocked)
                        time.sleep(0.5)

            else:
                vkbot.send_message(message='Чтобы начать напишите боту "старт"')
