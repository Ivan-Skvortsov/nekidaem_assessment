<div id="top"></div>
<div align="center">
<h1>Тестовое задание backend для Nekidaem </h1>
  <h3>
     Веб-приложение, которое реализует REST API.<br />
  </h3>
</div>

## О проекте
Функционал приложения:
1) Имеется база пользователей. У каждого пользователя при создании создается персональный блог.
2) Пост в блоге — запись с заголовком, текстом и временем создания.
3) Пользователь может подписываться/отписываться на блоги других пользователей
4) У пользователя есть персональная лента новостей (не более ~500 постов), в которой выводятся посты из блогов, на которые он подписан, в порядке добавления постов.
5) Пользователь может помечать посты в ленте прочитанными.
6) В ленте отображаются только непрочитанные посты
7) Раз в сутки на почту прилетает подборка из 5 последних постов ленты (реализован вывод в консоль)
8) Реализовано заполнение БД при помощи менеджмент-команд Django
9) Написаны тесты для эндпойнтов

## Использованные технологии и пакеты
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Celery](https://docs.celeryq.dev/en/stable/)
* [Redis](https://redis.io/)
* [Docker](https://www.docker.com/)

## Необходимый софт
Для развертывания проекта потребуется машина с предустановленным Docker и docker compose.<br/>
Инструкцию по установке можно найти на <a href="https://docs.docker.com/">официальном сайте</a>.

## Установка
Склонируйте проект на Ваш компьютер
   ```sh
   git clone https://github.com/Ivan-Skvortsov/nekidaem_assessment.git
   ```
Перейдите в папку с инструкциями docker compose
   ```sh
   cd nekidaem_assessment
   ```
Создайте файл с переменными окружения
   ```sh
   touch .env
   ```
Наполните файл следующими переменными
   ```sh
   DJANGO_SECRET_KEY # секретный ключ Django
   DJANGO_ALLOWED_HOSTS # перечень хостов, на которых развернуто приложение (через запятую)
   DJANGO_DEBUG # включени/отключени режима отладки Django  

   POSTGRES_DB # имя базы данных
   POSTGRES_USER # имя пользователя базы данных
   POSTGRES_PASSWORD # пароль пользователя базы данных
   DB_HOST # адрес хоста, на котором будет запущена база данных
   DB_PORT # порт хоста, на котором будет запущена база данных

   CELERY_BROKER_URL # адрес брокера сообщений (redis) для celery

   SEND_EMAILS_HOUR # час, в который будет запущена email-рассылка пользователям
   SEND_EMAILS_MINUTE # минуты, в которую будет запущена email-рассылка пользователям
   ```
   > **Note**:
   > Пример заполнения файла `.env` можно посмотреть в `.env.example`

Запустите контейнеры
   ```sh
   sudo docker compose -f docker-compose.yaml up -d
   ```
Создайте суперпользователя django (если это необходимо)
   ```sh
   sudo docker compose -f docker-compose.yaml exec backend python manage.py createsuperuser
   ```
Наполните базу данных тестовыми (фейковыми) данными (если это необходимо)
   ```sh
   sudo docker compose -f docker-compose.yaml exec backend python manage.py fill_database
   ```
   > **Warning**:
   > Заполнение возможно только на пустой базе данных. Если в БД присутствуют данные, начала необходимо их удалить, выполнив команду `sudo docker compose -f docker-compose.yaml python manage.py flush`

   > **Note**:
   > По умолчанию, команда `fill_database` создаёт 100 пользователей и 1000 постов. Если вам необходмио другое количество записей, укажите их в аргументах `--users`, `--posts`, например `sudo docker compose -f docker-compose.yaml python manage.py fill_database --users=500 --posts=3000`

## Использование приложения
### Ресурсы
1) Приложение будет доступно локально, по адресу http://localhost/
2) Админка доступна по адресу http://localhost/admin/ <br>
3) Документация API в интерактивной оболочке swagger доступна по адресу http://localhost/api/schema/swagger-ui/

   > **Note**:
   > При использовании Swagger, токен аутентификации необходимо передавать в формате `Token <ваш токен>`

В приложении реализованы ресурсы:
 ```sh
    GET /api/v1/posts/  # получить все посты
    POST /api/v1/posts/ # создать пост

    POST /api/v1/posts/{post_id}/seen/ # пометить пост прочитанным

    POST /api/v1/blogs/{blog_id}/follow/ # подписаться на блог
    POST /api/v1/blogs/{blog_id}/unfollow/ # отписаться от блога

    GET /api/v1/feed/ # персональная лента пользователя
```
### Аутентификация
Для упрощения, в проекте используется аутентифицаия по токену DRF. Есть несколько способов генерации токена:
1) В консоли, при помощи команды
   ```sh
   sudo docker compose -f docker-compose.yaml exec backend python manage.py drf_create_token <username>
   ```
2) В админке, по адресу http://localhost/admin/authtoken/tokenproxy/
   > **Note**:
   > При использовании Swagger, токен аутентификации необходимо передавать в формате `Token <ваш токен>`

### Периодические задачи по рассылке сообщений
В приложении реализована имитация email-рассылки. Фактически, письма не отправляются. Результат работы можно посмотреть в консоли `Celery`:
   ```sh
   sudo docker compose -f docker-compose.yaml logs celery
   ```

## Тестирование
Перейдите в папку с проектом
   ```sh
   cd nekidaem_assessment
   ```
Запустите тестовую базу данных
   ```sh
   sudo docker compose -f docker-compose.test.yaml up -d
   ```
Запустите тесты
   ```sh
   pytest -v
   ```

## Об авторе
Автор проекта: Иван Скворцов<br/><br />
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pprofcheg@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Profcheg)
