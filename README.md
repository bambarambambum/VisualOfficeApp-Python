# VisualOffice-App-Python
Пример микросервисного приложения на Python + Flask.
Приложение представляет из себя карту условного офиса, на котором можно редактировать рабочие места. Карта кликабельна.
Включает в себя снятие метрик (Prometheus)
## Внешний вид приложения
![Внешний вид приложения](https://i.ibb.co/XbT4nVb/screen.png)
Карта представляет собой SVG изображение, где у каждого рабочего места есть свой ID.
С помощью JavaScripts происходит обработка нажатий на карту.
## Сервисы
* webapp - Микросервис (веб-интерфейс) приложения, включающий в себя так же карту, на которой можно редактировать рабочие места.
* users_reader - Микросервис (читатель) приложения для получения данных из базы данных.
* users_writer - Микросервис (писатель) приложения для получения и сохранения данных в базу данных Postgres.
* db - Скрипт для заполнения базы данных Postgres тестовыми данными.
## Схема приложения
![Схема приложения](https://i.ibb.co/y0SzFRd/screen-scheme.png) 
WebApp обращается к микросервису users_reader (читатель) и получает список пользователей/пользователя из базы.
При наличии изменений - они отправляются микросервису users_writer, он записывает их в базу Postgres.
## CI
CI выполняется с помощью GitHub Actions. Происходит сборка и публикация docker-контейнеров.
