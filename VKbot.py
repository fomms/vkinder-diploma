import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

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

    def send_message(self, message, attachment=None, keyboard=None):  #метод упрощающая отправку сообщений
        self.vk.messages.send(
            user_id=self.user_id,
            message=message,
            random_id=randrange(10 ** 7),
            keyboard=keyboard,
            attachment=attachment
        )

    def send_candidate(self, candidate):
        if candidate[4] is None and candidate[5] is None:
            self.send_message(message=f'{candidate[0]} {candidate[1]} \n {candidate[2]} \n ',
                               attachment=candidate[3])  # отправляем кандидата пользователю
        elif candidate[5] is None:
            self.send_message(message=f'{candidate[0]} {candidate[1]} \n {candidate[2]} \n ',
                               attachment=','.join(candidate[3:4]))  # отправляем кандидата пользователю
        else:
            self.send_message(message=f'{candidate[0]} {candidate[1]} \n {candidate[2]} \n ',
                               attachment=','.join(candidate[3:5]))  # отправляем кандидата пользователю


    def get_started(self):  #метод начинающющий взаимодействие с человеком и получчающая его ID
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text
                if msg == 'старт':
                    self.user_id = event.user_id
                    return

    def get_info(self):  #метод получающий возраст поиска
        self.send_message(message='Введите минимальный возраст партнёра:')
        min_age = None
        max_age = None
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if min_age is None:
                    min_age = event.text
                    self.send_message(message='Введите максимальный возраст партнёра:')
                else:
                    max_age = event.text
                    return min_age, max_age
    
    def get_sex(self):  #метод получающий пол человека для поиска
        self.send_message(message='Введите пол человека которого хотите найти(мужской\женский):')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                sex = event.text
                if sex.lower() == 'женский':
                    return 1
                return 2

    def get_city(self):  #метод получающий город поиска
        self.send_message(message='Введите город поиска:')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                city = event.text
                self.send_message(message='Начинаем поиск...', keyboard=self.get_keyboard('button.json'))
                return city




