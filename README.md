# Hasker-Otus
The seventh hometask

## Описание

Q&A сайт, аналог stackoverflow.com

## Спецификация

### Структура приложения
Django сайт состоиз из двух приложений:
- Registration

Модуль, отвечает за регистрацию пользователя, авторизацию, возможность редактировать профайл пользователя.

- Question

Основной модуль. Для авторизированных пользователей есть возможность: задать вопрос, проголосовать за вопросы - ответы других пользователей, отозвать свой голос, выбрать правильный ответ для своего вопроса.

- API

Модуль, отвечает за API для приложения.

#### Запрос данных с index

    GET /api-v1/index/

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "title": "Вопрос 1",
            "body": "Как жить дальше",
            "create_date": "2020-09-06T18:18:33.935178+03:00",
            "author": "admin",
            "tags": [
                "жить дальше",
                " как",
                " Python"
            ]
        },
        {
            "title": "Вопрос 2",
            "body": "Жить дальше как",
            "create_date": "2020-09-06T18:19:16.398077+03:00",
            "author": "pupkin",
            "tags": [
                "Python"
            ]
        }
    ],
    "trends": [
        {
            "count": 2,
            "title": "Вопрос 1"
        },
        {
            "count": 1,
            "title": "Вопрос 2"
        }
    ]
}
```

#### Получение данных Question по id

    GET /api-v1/getquestion/1/

```json
{
    "title": "Вопрос 1",
    "body": "Как жить дальше",
    "create_date": "2020-09-06T18:18:33.935178+03:00",
    "author": "admin",
    "tags": [
        "жить дальше",
        " как",
        " Python"
    ]
}
```

#### Поиск Question

    GET /api-v1/searchresult/?search=1

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "title": "Вопрос 1",
            "body": "Как жить дальше",
            "create_date": "2020-09-06T18:18:33.935178+03:00",
            "author": "admin",
            "tags": [
                "жить дальше",
                " как",
                " Python"
            ]
        }
    ]
}
```

#### Получение ответов определенного ответа по id

    GET /api-v1/getanswers/1/

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "body": "Жить не тужить",
            "author": "pupkin",
            "create_date": "2020-09-06T18:28:11.858460+03:00",
            "correct": false
        },
        {
            "body": "ddfdfdf",
            "author": "pupkin",
            "create_date": "2020-09-07T18:16:06.207745+03:00",
            "correct": false
        }
    ]
}
```


## Запуск тестов

Для запуска тестов, запустите Командную строку, перейдите в папку с приложением (команда cd) и запустите команду "python manage.py test" (windows)

