"""Тестирование 97%."""

import json
import datetime
from http import HTTPStatus

from rest_framework.test import APITestCase
from django.utils import timezone

from project.celery import app


class TestsBase(APITestCase):

    def setUp(self):

        # celery в синхронный режим
        app.conf.update(CELERY_ALWAYS_EAGER=True)

    def test_api(self):

        now = timezone.now()

        # создание клиента
        resp = self.client.post("/api/v1/client/", {
                'phone_number': '73421767143',
                'timezone': 0,
                'code': 'AAA',
                'tag': 'BBB',
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(resp.content)['code'], 'AAA')

        # создание рассылки по коду с устаревшими сообщениями
        resp = self.client.post("/api/v1/distrib/", {
                'time_start': now,
                'time_end': now,
                'text': 'Just text',
                'filter_code': 'AAA',
                'filter_tag': ''
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(resp.content)['filter_code'], 'AAA')

        # создание рассылки по тегу с отправкой сообщений в течении дня
        resp = self.client.post("/api/v1/distrib/", {
                'time_start': now,
                'time_end': now + datetime.timedelta(days=1),
                'text': 'Just text',
                'filter_code': '',
                'filter_tag': 'BBB'
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(resp.content)['filter_tag'], 'BBB')

        # создание отложенной на 1 мин рассылки
        resp = self.client.post("/api/v1/distrib/", {
                'time_start': now + datetime.timedelta(minutes=1),
                'time_end': now + datetime.timedelta(days=1),
                'text': 'Just text',
                'filter_code': '',
                'filter_tag': 'BBB'
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(json.loads(resp.content)['filter_tag'], 'BBB')

        # общая статистика
        resp = self.client.get("/api/v1/stats/", follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(resp.content)['sended'], 3)

        # статистика по рассылке 1
        resp = self.client.get("/api/v1/stats/1", follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(resp.content)['sended'], 1)

        # статистика по не существующей рассылке
        resp = self.client.get("/api/v1/stats/5", follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(resp.content)['code'], 4)

        # частичное изменение клиента
        resp = self.client.patch("/api/v1/client/1/", {
                'timezone': 2,
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(resp.content)['timezone'], 2)

        # удаление клиента
        resp = self.client.delete(
            "/api/v1/client/1/", format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.NO_CONTENT)

        # частичное изменение рассылки
        resp = self.client.patch("/api/v1/distrib/1/", {
                'text': 'New text',
            }, format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(resp.content)['text'], 'New text')

        # удаление рассылки
        resp = self.client.delete(
            "/api/v1/distrib/1/", format='json', follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.NO_CONTENT)

