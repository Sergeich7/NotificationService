from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView

from rest_framework import routers

from .views import StatByDistributionAPIView, TotalStatAPIView
from .views import ClientViewSet, MessageViewSet, DistributionViewSet


router = routers.SimpleRouter()
router.register(r'client', ClientViewSet)
router.register(r'message', MessageViewSet)
router.register(r'distrib', DistributionViewSet)

urlpatterns = [

    path('', include(router.urls)),

    path('stats/', TotalStatAPIView.as_view(), name='stats-total'),
    path('stats/<int:id>', StatByDistributionAPIView.as_view(), name='stats-dist'),

    # API документация
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
