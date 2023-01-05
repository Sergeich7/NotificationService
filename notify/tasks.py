import datetime
import requests

from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail

from django.conf import settings
from project.celery import app
from .models import Message, Client, Distribution


@app.task
def send_one_notify(distribution_id: int, client_id: int):
    """Отправка одного сообщения."""
    distribution = Distribution.objects.get(pk=distribution_id)
    client = Client.objects.get(pk=client_id)

    # Создаем сообщение в базе
    now = timezone.now()
    message = Message(created=now, client=client, distribution=distribution,)
    message.save()

    if distribution.time_start < now < distribution.time_end:
        s_head = {      # заголовок запроса
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(settings.TOKEN), }
        s_data = {      # тело запроса
            'id': message.id,
            'phone': int(client.phone_number),
            'text': distribution.text, }
        try:
            # Запрос
            res = requests.post(
                f'https://probe.fbrq.cloud/v1/send/{message.id}',
                json=s_data, headers=s_head).json()
        except:
            # Ошибка сети
            res = {'code': 1, 'message': 'Network error'}
        finally:
            pass
    else:
        res = {'code': 2, 'message': 'Message expired'}

    # Сохраняем результат выполнения запроса
    message.status = res
    message.save()


def recipients(distribution_id: int):
    """Выбираем получателей рассылки по фильтру."""
    dist = Distribution.objects.get(pk=distribution_id)

    q = Q()
    if dist.filter_code:
        q = q & Q(code=dist.filter_code)
    if dist.filter_tag:
        q = q & Q(tag=dist.filter_tag)
    return Client.objects.filter(q)


@app.task
def make_distribution(distribution_id: int):
    """Создаем задачи на отправку сообщений."""
    clients = recipients(distribution_id)

    for client in clients:
        send_one_notify.delay(distribution_id, client.id)


@app.task
def send_daily_stats():
    """Отправляем статистику за вчера."""
    yesterday = timezone.now() - datetime.timedelta(days=1)
    dist_count = Distribution.objects.filter(
        time_start__year=yesterday.year,
        time_start__month=yesterday.month,
        time_start__day=yesterday.day
    )
    mess_count = Message.objects.filter(
        created__year=yesterday.year,
        created__month=yesterday.month,
        created__day=yesterday.day
    )

    # Отправляем письмо
    return send_mail(
        f'Daily Stats {yesterday.date()}',
        f'Distributions: {dist_count} Messages: {mess_count}',
        settings.SERVER_EMAIL,
        [settings.SERVER_EMAIL,],
        fail_silently=False,
    )
