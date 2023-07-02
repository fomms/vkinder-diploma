import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from VKapi import VKapi


class VKbot:

    def __init__(self, token):
        self.token = token
        self.session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()

    @staticmethod  #статичный метод для вывода клавиатуры
    def get_keyboard(path):
        with open(path, "r", encoding="UTF-8") as f:
            data = f.read()
            return data

    def send_message(self, user_id, message, attachment=None, keyboard=None):  #метод упрощающая отправку сообщений
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7),
            keyboard=keyboard,
            attachment=attachment
        )

    def get_started(self):  #метод начинающющий взаимодействие с человеком и получчающая его ID
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text
                if msg == 'старт':
                    self.user_id = event.user_id
                    return

    def get_info(self):  #метод получающий возраст поиска
        self.send_message(self.user_id, message='Введите минимальный возраст партнёра:')
        min_age = None
        max_age = None
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if min_age is None:
                    min_age = event.text
                    self.send_message(event.user_id, message='Введите максимальный возраст партнёра:')
                else:
                    max_age = event.text
                    return min_age, max_age

    def get_city(self):  #метод получающий город поиска
        self.send_message(self.user_id, message='Введите город поиска:')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                city = event.text
                self.send_message(self.user_id, message='Начинаем поиск...', keyboard=self.get_keyboard('button.json'))
                return city


    # def searching_for_pair(self):#не уверен что чтоит основной код делать методом класса возможно лучше просто в мэйн
    #     for event in self.longpoll.listen():
    #         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    #             msg = event.text
    #
    #             if msg == 'NEXT':
    #                 """ отправляем пользователю сообщение с дынными в формате
    #                 name surname
    #                 link
    #                 ссылки на фото разделенные запятой"""
    #             elif msg == 'ADD_TO_FAVOURITE':
    #                 """меняем в последнем кандидате параметр FAVOURITE"""
    #                 self.send_message(self.user_id, message='Анкета добавлена в избранное!')
    #             elif msg == 'ADD_TO_BLACK_LIST':
    #                 """меняем в последнем кандидате параметр BLACK_LIST"""
    #                 self.send_message(self.user_id, message='Анкета добавлена в заблокированное!')
    #             elif msg == 'SHOW_FAVOURITE':
    #                 """показаваем человеку всех в избранном"""
    #             elif msg == 'SHOW_BLACK_LIST':
    #                 """показаваем человеку всех в заблокированном"""





