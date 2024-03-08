#  Финпльный проект Kittygram

## Описание проекта

Китиграм - социальная сеть, для обмена фото и достижениями котиков)

## Функционал проекта

Пользователь может зарегистрироваться и добавлять информация о своих (а может не своих) котиков. 

Автор может редактировать и удалять "карточки" котиков.

Анонимный пользователь может только просматривать "карточки" котиков.

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
cd kittigram_final

# Запустить автоматическое скачивание и развёртывание контейнеров
sudo docker compose -f docker-compose.production.yml pull

# В случае, если контейнеры уже скачаны и запрущены
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

### Примеры запросок к API

```javascript
// Получить список котиков на определённой странице
GET /api/cats/?page={page_number}
    headers: {
      "Content-Type": "application/json",
      authorization: "Token auth_token",
    }

// Получить карточку конкретного котика
GET /api/cats/{cat_id}/
    headers: {
      "Content-Type": "application/json",
      authorization: "Token auth_token",
    }

// Создать карточку котика, без изображения и достижений
POST /api/cats/
    headers: {
      "Content-Type": "application/json",
      authorization: "Token auth_token"
    }
    body: {
        "name": "Имя котика",
        "birth_year": "Год рождения котика",
        "color": "Цвет котика"
    }
```
