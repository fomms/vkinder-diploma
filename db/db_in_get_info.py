import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db.models import create_tables
from db.models import UserVKTinder, SearhPair, SearhPairPhoto
from vk_api_my import VKAPIusers
from tokens import Password_db


Login_db = 'postgres'
Name_db = 'test'

DSN = f"postgresql://{Login_db}:{Password_db}@localhost:5432/{Name_db}"
engine = sqlalchemy.create_engine(DSN)  # Создание движка
create_tables(engine)  # создание таблиц
Session = sessionmaker(bind=engine)
session = Session() #создание текущей сессии (в объявлениях функций передается как connection)


def add_user(user_id):
    ''' Функция добавления текущего юзера в БД'''
    info_list = VKAPIusers.get_vktinder_user(user_id) #получение данных о пользователе приложением из вк апи по его id(функция вызывается из модуля vk_api_my)
    users = UserVKTinder(user_vk_id=info_list[0]['id'], # преобразование пользователя в экземпляра класса UserVKTinder
                        user_vktinder_name=info_list[0]['first_name'],
                        user_vktinder_surname=info_list[0]['last_name'])
    session.add(users)
    session.commit() #фиксация изменений в БД


def check_user(connection, user_id):
    ''' Функция проверяет находится ли данный юзер в БД'''
    querys = connection.query(UserVKTinder.user_vk_id).filter(UserVKTinder.user_vk_id == user_id).first()
    return querys


def add_new(searh_users, user_id):
    objects_list = []
    for user in searh_users: #преобразование пользователя в экземпляра класса SearhPair
        info = SearhPair(
                searh_pair_name=user["name"],
                searh_pair_surname=user["surname"],
                searh_pair_page_link=user["page_link"],
                searh_pair_vk_id=user["id"],
                user_vktinder_id=user_id, # здесь происходит связывание искомого человека с тем кто его ищет (один ко многим)
                attribute=0
                )
        objects_list.append(info)
        session.add_all(objects_list)
        session.commit()
        if len(user["photo"]) == 0: # здесь происходит связывание искомого человека с его фото (один ко многим)
            photo = SearhPairPhoto(searh_pair_id=info.searh_pair_id)
            objects_list.append(photo)
        elif len(user["photo"]) == 1:
            photo = SearhPairPhoto(searh_pair_id=info.searh_pair_id, photo_1=user["photo"][0])
            objects_list.append(photo)
        elif len(user["photo"]) == 2:
            photo = SearhPairPhoto(searh_pair_id=info.searh_pair_id, photo_1=user["photo"][0], photo_2=user["photo"][1])
            objects_list.append(photo)
        elif len(user["photo"]) == 3:
            photo = SearhPairPhoto(searh_pair_id=info.searh_pair_id, photo_1=user["photo"][0], photo_2=user["photo"][1],
                                   photo_3=user["photo"][2])
            objects_list.append(photo) 
        session.add_all(objects_list)
        session.commit()  # фиксация изменений в БД
    session.close()


def get_new_searh_pair_info(connection, user_vk_id):
    '''для получения новых кандидатов после просмотра старых'''
    querys = connection.query(SearhPair.searh_pair_name, SearhPair.searh_pair_surname, SearhPair.searh_pair_page_link,
                              SearhPairPhoto.photo_1, SearhPairPhoto.photo_2, SearhPairPhoto.photo_3).join(
        SearhPair).join(UserVKTinder).filter(UserVKTinder.user_vk_id == user_vk_id, SearhPair.attribute == 0).all()

    return querys


def update_db_attribute(connection, user_vktinder_id, searh_pair_id, attribute):
    '''Функция изменения параметра атрибут (attribute) в БД. На вход принимает связь с БД т.е сессию(session), id VK как пользователя приложения, так и искомого человека, а так же знвчение аттрибута:
    типа int: 1 - в список понравившихся, 2 - черный список'''
    update_searh_pair_id = connection.query(SearhPair.searh_pair_id).join(UserVKTinder).filter(SearhPair.searh_pair_vk_id == searh_pair_id, UserVKTinder.user_vk_id == user_vktinder_id).all()
    connection.query(SearhPair).filter(SearhPair.searh_pair_id == update_searh_pair_id[0][0]).update({"attribute": attribute})
    session.commit()
    session.close()

def get_list_likes_pair(connection, user_vk_id):
    '''Функция получения информации о пользователях для выдачи в приложении добавленных в список понравившихся (имеющих attribute == 1)
    Принимает на вход связь с БД т.е сессию(session) и VK id пользователя приложения. Возвращает список.'''
    list_likes_pair = connection.query(SearhPair.searh_pair_name, SearhPair.searh_pair_surname, SearhPair.searh_pair_page_link,
                    SearhPairPhoto.photo_1, SearhPairPhoto.photo_2, SearhPairPhoto.photo_3).join(SearhPair).join(UserVKTinder).filter(UserVKTinder.user_vk_id == user_vk_id, SearhPair.attribute == 1).all()
    return list_likes_pair

def get_list_blocked_pair(connection, user_vk_id):
    '''Функция получения информации о пользователях для выдачи в приложении добавленных в список заблокированных (имеющих attribute == 2)
    Принимает на вход связь с БД т.е сессию(session) и VK id пользователя приложения. Возвращает список.'''
    list_blocked_pair = connection.query(SearhPair.searh_pair_name, SearhPair.searh_pair_surname, SearhPair.searh_pair_page_link,
                    SearhPairPhoto.photo_1, SearhPairPhoto.photo_2, SearhPairPhoto.photo_3).join(SearhPair).join(UserVKTinder).filter(UserVKTinder.user_vk_id == user_vk_id, SearhPair.attribute == 2).all()
    return list_blocked_pair

