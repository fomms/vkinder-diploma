
from VKbot import VKbot
from vk_api.longpoll import VkEventType
from tokens import access_token, group_token
from vk_api_my import VKAPIusers

vkbot = VKbot(group_token)

vkbot.get_started()
min_age, max_age = vkbot.get_info()
city = vkbot.get_city()

vkapi = VKAPIusers(min_age, max_age, city, sex=1)

print(vkapi.search_users())





# for event in vkbot.longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW and event.to_me:
#         msg = event.text
#
#         if msg == 'NEXT':
#             """ отправляем пользователю сообщение с дынными в формате
#             name surname
#             link
#             ссылки на фото разделенные запятой"""
#         elif msg == 'ADD_TO_FAVOURITE':
#             """меняем в последнем кандидате параметр FAVOURITE"""
#             vkbot.send_message(vkbot.user_id, message='Анкета добавлена в избранное!')
#         elif msg == 'ADD_TO_BLACK_LIST':
#             """меняем в последнем кандидате параметр BLACK_LIST"""
#             vkbot.send_message(vkbot.user_id, message='Анкета добавлена в заблокированное!')
#         elif msg == 'SHOW_FAVOURITE':
#             """показаваем человеку всех в избранном"""
#         elif msg == 'SHOW_BLACK_LIST':
#             """показаваем человеку всех в заблокированном"""