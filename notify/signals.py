"""Обработка сигналов."""

from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

from .models import Distribution
from .tasks import make_distribution

import logging
logger = logging.getLogger('trace')


@receiver(signals.post_save, sender=Distribution)
def create_distribution(sender, instance, created, **kwargs):
    """Создаем задачу на создание рассылки."""
    now = timezone.now()

    start_after = 1
    if instance.time_start > now:
        # Откладываем рассылку до времени старта
        start_after = int((instance.time_start - now).total_seconds())

    make_distribution.apply_async([instance.id,], countdown=start_after)
    logger.info(f'DISTRIBUTION:{instance.id} created. Start over {start_after} sec.')
