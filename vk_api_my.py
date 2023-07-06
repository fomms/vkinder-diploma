import vk_api
from tokens import access_token
import os
import time

class VKAPIparent:

    session = vk_api.VkApi(token=access_token)
    vk = session.get_api()


class VKAPIusers(VKAPIparent):
    '''Класс для работы с пользователями ВК. Для работы необходим токен для соединения с api.'''

    def __init__(self, age_from: int, age_to: int, city: int, sex: int, offset=0) -> None: # инициализация экземпляров класса
        super().__init__()
        self.age_from = age_from  # возвраст от
        self.age_to = age_to  # возвраст до
        self.city = city  # город id города
        self.sex = sex  # пол 1 — женщина, 2 — мужчина, 0 — любой
        self.offset = offset

    def get_search_params(self): # метод ввода информации о параметрах поиска человека(параметра берутся из self,  тюк они проинициализированы)
        return {
            'age_from': self.age_from,
            'age_to': self.age_to,
            'hometown': self.city,
            'sex': self.sex,
            'status': 1,
            'count': 3,
            'has_photo': 1,
            'offset': self.offset
            }

    def get_vktinder_user(id): # метод получения информации о пользователе приложения по его id
        user_get = VKAPIparent.vk.users.get(user_ids=id, fields=('city', 'bdate'))
        return user_get

    def get_user_photo(self, id):  # метод получения фотографий пользователя)
        photo_list = []
        photos = self.session.method('photos.get', {'owner_id': id, 'album_id': 'profile', 'photo_sizes': 1, 'count': 500, 'extended': 1})
        for photo in photos["items"]:
            photo_dict = {
                'photo_link': photo["sizes"][-1]["url"],
                'likes': photo["likes"]['count']
            }
            photo_list.append(photo_dict)
        photo_list_sort = sorted(photo_list, key=lambda x: x['likes']) # сортировка по лайкам
        return [link['photo_link'] for link in photo_list_sort][:3] # возвращает список из трех элеметов

    def search_users(self):  # метод для поиска людей в соотвествии с параметрами, принимает на вход self
        users_list = []
        self.response = self.session.method("users.search", {**self.get_search_params()})

        for user in self.response['items']:
            if user['is_closed'] is True:
                continue
            users_info = {
                'id': user['id'],
                'page_link': f'https://vk.com/id{user["id"]}',
                'name': user['first_name'],
                'surname': user['last_name'],
                'photo': self.get_user_photo(user['id'])}
            users_list.append(users_info)
        return users_list  #возвращает список пользователей


# start = time.time()
#
# # access_token = os.getenv('access_token')
# print(access_token)
# vkapi = VKAPIusers(18, 20, 1, 1)
# print(vkapi.search_users())
# print(vkapi.get_vktinder_user())
# print(vkapi.search_users())
#
# end = time.time()
# print(end - start)