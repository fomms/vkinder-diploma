# ВК бот VKinder
 
 Приложение VKinder - универсальное приложение для управления сообществом в социальной сети Вконтакте. Оно предназначено для подбора наиболее подходящих профилей ВК для человека по критериям поиска (минимальный и максимальный возвраст искомого человвека, город проживания, его пол).
### Начало работы ###
 Для корректной работы приложения необходимо получить два токена от ВК:
 1. Для работы с [VK API](https://dev.vk.com/api/access-token/getting-started)
 2. Для работы вашего [сообщества - бота ВК типа VkLongPoll](https://dev.vk.com/api/bots/getting-started#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0). Полученные токены вставьте в файл  tokens.py в соответствующие переменные.

Для работы приложения на сервере установите необходимые зависимости из файла requirements.txt.
Логика работы бота построена на основе python скрипта VKinder - diploma.
### Основные модули и логика их работы ###
1. **Модуль vk_api_my** предназначен для описания логики работы бота и взаимодействия его с [ВК api](https://dev.vk.com/reference). Класс VKAPIparent - создан для подключения к api ВК через объект сессии. Подключение происходит за счёт access_token полученного ранее. *Класс VKAPIusers* предназначен для непосредственной работы с [методами api ВК](https://dev.vk.com/method), для извлечения необходимых данных о пользователях. Каждый экземпляр класса содеожит необходимую информацию о пользователях которую необходимо применить для поиска. Метод *get_vktinder_user()* предназначен для получения информации о пользователе приложения по его id. Метод *search_users()* служит для поиска анкет пользователей в соответствии с с параметрами экземпляра класса. Подача параметров для поиска происходит через метод *get_search_params*, который преобразует свойства экземпляра класса в параметры передаваемые в ВК api. Метод *get_user_photo* получает фотографии пользователей найденных в соответствии с параметрами поиска, сортирует их по количеству лайков и выдает боту три самых популярных фотографии.  
2. **Модуль VKbot** содержит в себе описание класса *VKbot* предназначенного для взаимодействия внутренней логики бота с пользователем. Взаимодеиствие построено на VkLongPoll запросах которые ожидают событие полученное от пользователя. основой взаимодействия являются отправка сообщений пользователем которые воспринимаются ботом как Event событие, с ответной реакцией бота. Каждый экземпляр класса бота принимает на вход токен группы из файла tokens.py на основе чего создается сессия которая взаимодействует с ботом. Основные методы класса: *get_keyboard* - метод считывающий jsonфайл с характеристиками кнопок для взаимодействия с ботом, *send_message* - метод определяющий порядок и параметры отправляемых боту сообщений, *send_candidate* - метод определяющий порядок и форму выдачи информации, о найденных людях, *get_started* - метод получения ID пользователя написавшего боту, кроме того с него начинается взаимодействие человека и бота, *get_min_age, get_max_age* - метод получения информации от пользователя о желаемом минимальном и максимальном возврасте искомого человека, реализована проверка на то чтобы пользователь вводил в графу возвраст именно числа, в противном случае бот предложит изменить значение, *get_sex* - метод получения и ввода пола человека, *get_city* - метод получения от пользователя города для поиска.
3. В папке db(database) содержаться модули для организации работы бота с базой данных. В программе прилменяется СУБД Postgres. Перед установкой скрипта на сервере необходимо создать БД. Данные о названии БД, логине и пароле для управления БД необходимо предварительно записать в файл   tokens.py в соответствующие графы. Логика работы с БД построена на абстракции ORM  на основе библиотеки SQLAlchemy, а подключение Postgres к интерпритатору Python построено на драйвере psycopg2. **Модуль models** содержит в себе три класса и реализован по [схеме](VKtinder.jpeg) отражающую всю информацию о пользователе приложения *UserVKTinder* и связанных с ним найденных анкет пользователей *SearhPair*, организованных по связи типа один ко  многим. Связь *UserVKTinder с SearhPair* происходит по ключу ВК ID имеющим свойство уникальности. Анкета каждого пользователя кандидата связана с таблицей c фотографиями этих пользователей *SearhPairPhoto*. **Модуль bd_in_get_info** содержит в себе функции для заполнения и работы с данными содержащимися в БД. Функция *add_user* добавляет в таблицу UserVKTinder данные о пользователе приложения. Данные берутся с помощью метода *get_vktinder_user* из api ВК. Функция *check_user* проверяет есть ли данный пользователь уже в БД. Функция *add_new* для добавления новых найденных пользователей в БД. *get_new_searh_pair_info* функция  для получения новых кандидатов после просмотра старых. *update_db_attribute* - функция изменения параметра атрибут (attribute) в БД. На вход принимает связь с БД т.е сессию(session), id VK как пользователя приложения, так и искомого человека, а так же знвчение аттрибута: типа int: 1 - в список понравившихся, 2 - черный список, 3 - просмотренные. *get_list_likes_pair* - функция получения информации о пользователях для выдачи в приложении добавленных в список понравившихся (имеющих attribute == 1). *get_list_blocked_pair* - функция получения информации о пользователях для выдачи в приложении добавленных в список заблокированных (имеющих attribute == 2) принимает на вход связь с БД т.е сессию(session) и VK id пользователя приложения. Возвращает список.
4. Для организации просмотра пользователем анкет по одной, в программе реализован итератор по списку пользователей кандидатов, с целью экономии памяти устройства. порядок работы итератора - последовательноость выдачи анкет смоделирована в модуле iterator.py  с классом PeopleIterator, с прописанными там методами next  и iter.
5. В **модуле main** происходит создание ранее описанных экземпляров классов для работы с ВК api и бота для взаимодействия с пользователем. Далее прописана логика вызова соответствующих функций в зависимости от поведения и действий пользователя. Пользовватель взаимодействует с ботом через возбуждение событий в длинных LongPoll запросов. В приложении используется event.type == VkEventType.MESSAGE_NEW сообщения, для возбуждения бота и совершения им действий в приложении. 
6. Работа приложения инициируется пользователем введением сообщения  - **"старт"**, после чего бот начинает запрашивать параметры для подбора кандидатов, взаимодействия с api а так же записи результатов в БД, и выдачи их пользователю, изменения атрибута пользователя в соответствии с желаниями пользователя.

Наше приложение имеет огромный потенциал для развития.
    