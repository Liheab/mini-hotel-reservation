from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet

router = DefaultRouter(trailing_slash=False)
router.register("rooms", RoomViewSet)
router.register("bookings", BookingViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
