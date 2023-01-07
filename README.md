## NotificationService
Сервис управления рассылками, API администрирования и получения статистики. 

### При разработки использовал
Python, Django framework, Django REST framework, SQLite, Redis, Celery, RabbitMQ, Git, Docker, Docker compose. 

### Установка и запуск
* git clone https://github.com/Sergeich7/NotificationService.git
* cd NotificationService
* Необходимо создать файл .env на основе .env.sample с вашим токеном от сервиса уведомлений и акком для отправки почты
* docker-compose up --build -d

### API Сервиса
* http://localhost:8000/api/v1/schema/swagger-ui/
* http://localhost:8000/api/v1/schema/redoc/
* http://localhost:8000/api/v1/schema/

### Управление
* Админка Django (admin/admin): http://localhost:8000/admin/
* Celery (статистика и результаты):  http://localhost:5555/
* Админка RabbitMQ (guest/guest): http://localhost:15672/

### Задание
Необходимо разработать сервис управления рассылками API администрирования и получения статистики, который по заданным правилам запускает рассылку по списку клиентов:
* Необходимо реализовать методы создания новой рассылки, просмотра созданных и получения статистики по выполненным рассылкам.
* Реализовать сам сервис отправки уведомлений на внешнее API.

Сущность "рассылка" имеет атрибуты:
* уникальный id рассылки
* дата и время запуска рассылки
* текст сообщения для доставки клиенту
* фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
* дата и время окончания рассылки: если по каким-то причинам не успели разослать все сообщения - никакие сообщения клиентам после этого времени доставляться не должны

Сущность "клиент" имеет атрибуты:
* уникальный id клиента
* номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
* код мобильного оператора
* тег (произвольная метка)
* часовой пояс

Сущность "сообщение" имеет атрибуты:
* уникальный id сообщения
* дата и время создания (отправки)
* статус отправки
* id рассылки, в рамках которой было отправлено сообщение
* id клиента, которому отправили

Спроектировать и реализовать API для:
* добавления нового клиента в справочник со всеми его атрибутами
* обновления данных атрибутов клиента
* удаления клиента из справочника
* добавления новой рассылки со всеми её атрибутами
* получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
* получения детальной статистики отправленных сообщений по конкретной рассылке
* обновления атрибутов рассылки
* удаления рассылки
* обработки активных рассылок и отправки сообщений клиентам

Логика рассылки
* После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания - должны быть выбраны из справочника все клиенты, которые подходят под значения фильтра, указанного в этой рассылке и запущена отправка для всех этих клиентов.
* Если создаётся рассылка с временем старта в будущем - отправка должна стартовать автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.
* По ходу отправки сообщений должна собираться статистика (см. описание сущности "сообщение" выше) по каждому сообщению для последующего формирования отчётов.
* Внешний сервис, который принимает отправляемые сообщения, может долго обрабатывать запрос, отвечать некорректными данными, на какое-то время вообще не принимать запросы. Необходимо реализовать корректную обработку подобных ошибок. Проблемы с внешним сервисом не должны влиять на стабильность работы разрабатываемого сервиса рассылок.
Для интеграции с разрабатываемым проектом в данном задании существует внешний сервис, который может принимать запросы на отправку сообщений в сторону клиентов. OpenAPI спецификация находится по адресу: https://probe.fbrq.cloud/docs. В этом API предполагается аутентификация с использованием JWT.

### Дополнительно
1 СДЕЛАНО 97% организовать тестирование написанного кода

3 СДЕЛАНО подготовить docker-compose для запуска всех сервисов проекта одной командой

5 СДЕЛАНО сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io

8 СДЕЛАНО реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email

12 СДЕЛАНО <a href='https://github.com/Sergeich7/NotificationService/blob/master/trace.log'>trace.log</a> обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по
* id рассылки - все логи по конкретной рассылке (и запросы на api и внешние запросы на отправку конкретных сообщений)
* id сообщения - по конкретному сообщению (все запросы и ответы от внешнего сервиса, вся обработка конкретного сообщения)
* id клиента - любые операции, которые связаны с конкретным клиентом (добавление/редактирование/отправка сообщения/…)
