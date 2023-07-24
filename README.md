## Foodgram – продуктовый помошник

Cайт  доступен по ссылке: http://it-home.shop
```
Суперюзер
Логин: reviewerlogin
Пароль: reviverpassword
```
Документация к API по ссылке: http://it-home.shop/api/docs/

## О проекте
На этом сервисе пользователи смогут:
- публиковать рецепты
- подписываться на публикации других авторов
- добавлять понравившиеся рецепты в список «Избранное»
- скачивать сводный список продуктов для покупок

## Стек технологий

![python version](https://img.shields.io/badge/Python-3.7-yellowgreen)
![python version](https://img.shields.io/badge/Django-3.2.15-yellowgreen)
![python version](https://img.shields.io/badge/djangorestframework-3.13.1-yellowgreen)
![python version](https://img.shields.io/badge/djoser-2.1.0-yellowgreen)
![python version](https://img.shields.io/badge/gunicorn-20.1.0-yellowgreen)
![python version](https://img.shields.io/badge/psycopg2--binary-2.9.2-yellowgreen)

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке

```
https://github.com/amigovlg/foodgram-project-react.git
cd foodgram-project-react
```

Перейти в папку "infra" <br>
```
cd infra
```
Заполнить файл ".env" собственными настройками БД <br>
Запустить контейнеры

```
docker-compose up -d --build
```

В скрипте автоматически выполнятся задачи миграции, подключения статики и наполнение базы демонстрациооными данными

Запустить в браузере

```
http://localhost/
```