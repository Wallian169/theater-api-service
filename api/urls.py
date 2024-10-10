from django.urls import path, include
from rest_framework import routers

from api.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TheatreHallViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("theatre-halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "api"
