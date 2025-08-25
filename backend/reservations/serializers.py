from rest_framework import serializers
from datetime import date

from reservations.constants import RoomType
from reservations.models import Booking, Room, Guest
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer


class AmenitiesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True)
    room_type = serializers.ChoiceField(
        choices=RoomType.choices,
        error_messages={
            "invalid_choice": "Selected room type is invalid. Please choose from Single or Double."
        },
    )

    class Meta:
        model = Room
        fields = "__all__"
        extra_kwargs = {
            "number": {"required": True, "allow_null": False},
            "price": {"required": True, "allow_null": False},
            "capacity": {"required": True, "allow_null": False},
            "description": {"required": False, "allow_null": True},  # optional
        }

    def validate(self, data):
        capacity = data.get("capacity", None)

        if capacity is not None and capacity < 1:
            raise serializers.ValidationError(
                {"capacity": "Room capacity must be at least 1."}
            )

        return data


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"


class BookingSerializer(WritableNestedModelSerializer):
    room = PresentablePrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        presentation_serializer=RoomSerializer,
    )
    guest = GuestSerializer()

    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "total_price": {"required": False, "allow_null": True},  # calculated field
        }

    def validate(self, data):
        room = data.get("room", None)
        current_date = date.today()
        check_in = data.get("check_in", current_date)
        check_out = data.get("check_out", current_date)

        if check_out < check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            room=room, check_in__lt=check_out, check_out__gt=check_in
        )
        if overlapping.exists():
            raise serializers.ValidationError("Room is already booked for these dates.")

        return data
