
#  Финaльный проект FoodGram

Проект доступен по адресу: [https://bondarenko-foodgram.sytes.net/](https://bondarenko-foodgram.sytes.net/)

## Описание проекта

Фудграм - социальная сеть, для обмена рецептами

## Функционал проекта

Пользователь может зарегистрироваться и добавлять свои рецепты, подписываться на других авторов, составлять список покупок, добавлять рецепты в избранное. 

Автор может полностью управлять своими рецептами (удалять/создавать/редактировать).

Анонимный пользователь может только просматривать рецепты.

## Инструкция по запуску проекта

Проект работает в контейнерах на базе Docker.

Для того, чтобы автоматически развернуть и запустить проект в своем индивидуальном окружении необходимо выполнить следующие команды:

## Установка Docker и Docker Compose
### Подготовка Windows к установке Docker
Сделать доступным Linux-ядро в Windows можно двумя способами:
- Установить Windows Subsystem for Linux (WSL). WSL доступна для Windows 10 и 11. Текущая версия WSL — вторая, сокращённо — WSL2
- Развернуть виртуальную машину с Linux
- Есть ещё один вариант — настроить гипервизор Hyper-V.

Если у вас Windows 10 или 11, выбирайте вариант с Windows Subsystem for Linux, у него есть несколько преимуществ:
быстрее в установке, чем виртуальная машина с Linux;
работает внутри основной операционной системы — все приложения доступны сразу, не нужно заходить в виртуальную машину.

Если же вы работаете на Windows 8 или на более ранних версиях, устанавливайте виртуальную машину и разворачивайте на ней Linux.

#### После установки WSL: установка Docker на Windows
Зайдите на [официальный сайт](https://www.docker.com/products/docker-desktop/) проекта и скачайте установочный файл Docker Desktop.

Запустите его: на ваш компьютер будет установлена программа для управления контейнерами (докер-демон) и докер-клиенты — графический интерфейс и интерфейс командной строки.

## Установка Docker на Linux
В терминале введите следующие команды:
```Bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh 
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
```
## Развёртывание проекта
Перед развёртыванием проекта необходимо, в корневую директории проекта, скачать файл "docker-compose.production",
после чего необходимо, в корневой директории, где находится файл "docker-compose.production", создать файл .env

Описание содержимого .env-файла есть в файле ".env.example"
```Bash
# Перейти в корневую директорию проекта
cd foodgram

# Запустить автоматическое скачивание
sudo docker compose -f docker-compose.production.yml pull

# В случае, если контейнеры уже скачаны
sudo docker compose -f docker-compose.production.yml down

sudo docker compose -f docker-compose.production.yml up -d
```

Контейнеры скачаются и запустятся автоматически.

Миграции и установка статики произойдут автоматически.

Все работает "из коробки" ;)

## Прочая информация
Автор: Бондаренко В. В.

Backend: Django
- Gunicorn
- Django Rest Framework
- Djoser
- Webcolor

Frontend: React
- React Router Dom
- Web Vitals
- React Scripts

### Информация для ревьювера

Суперпользователь (создаётся автоматически, для удаления функции удалить блок создания пользователя из start_server.sh):
```bash
login: admin
password: admin
email: admin@admin.com

От его имени так же есть рецепты
```

Тестовые пользователи:
```bash
email: te2st@test.com
password: TestTest8
```
```bash
email: te2st2@test.com
password: TestTest8
```

Не много не понял, фронтенд работает не так или я где-то не прав, но:

При попытке, неавторизованного пользователя, зайти на страницу любого другого - происходит редирект на страницу логина.

При тесте API доступ к данным пользоваталей, неавторизованными, есть и ответ верен.
