from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Client, Message, Distribution
from .serializers import ClientSerializer, MessageSerializer
from .serializers import DistributionSerializer
from .tasks import recipients


@extend_schema_view(
    list=extend_schema(summary='Список всех получателей'),
    create=extend_schema(summary='Создание получателя'),
    retrieve=extend_schema(summary='Детальные данные получателя'),
    update=extend_schema(summary='Создание/изменение получателя'),
    partial_update=extend_schema(summary='Изменение получателя'),
    destroy=extend_schema(summary='Удаление получателя'),
)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


@extend_schema_view(
    list=extend_schema(summary='Список всех сообщений'),
)
class MessageViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


@extend_schema_view(
    list=extend_schema(summary='Список всех рассылок'),
    create=extend_schema(summary='Создание рассылоки'),
    retrieve=extend_schema(summary='Детальные данные по рассылке'),
    update=extend_schema(summary='Создание/изменение рассылки'),
    partial_update=extend_schema(summary='Изменение рассылки'),
    destroy=extend_schema(summary='Удаление рассылки'),
)
class DistributionViewSet(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(
            {'distribution': 'created'},
            status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(summary='Статистика по рассылке'),
)
class StatByDistributionAPIView(APIView):

    def get(self, request, id):
        try:
            Distribution.objects.all().get(pk=id)
        except ObjectDoesNotExist:
            data = {    
                'code': 4,
                'message': f'Distribution {id} Does not exist',
            }
        else:
            data = {
                'distribution': id,
                'recipients': len(recipients(id)),
                'sended': Message.objects.filter(distribution=id).count(),
                'status_0_ok': Message.objects.filter(distribution=id).filter(status__code=0).count(),
                'error_1_network': Message.objects.filter(distribution=id).filter(status__code=1).count(),
                'error_2_expired': Message.objects.filter(distribution=id).filter(status__code=2).count(),
            }
        finally:
            return Response(data)


@extend_schema_view(
    get=extend_schema(summary='Общая статистика'),
)
class TotalStatAPIView(APIView):

    def get(self, request):
        data = {
            'distributions': Distribution.objects.all().count(),
            'recipients': Client.objects.all().count(),
            'sended': Message.objects.all().count(),
            'status_0_ok': Message.objects.filter(status__code=0).count(),
            'error_1_network': Message.objects.filter(status__code=1).count(),
            'error_2_expired': Message.objects.filter(status__code=2).count(),
        }
        return Response(data)
