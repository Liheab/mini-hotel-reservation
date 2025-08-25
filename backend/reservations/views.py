import django_filters
from rest_framework import viewsets
from rest_framework.response import Response
from reservations.models import Booking, Room
from reservations.serializers import RoomSerializer
from reservations.serializers import BookingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        queryset = self.get_queryset()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
