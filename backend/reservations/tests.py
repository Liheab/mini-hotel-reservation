from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Room, Booking, Guest
import datetime


class RoomAndBookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a Room directly
        self.room = Room.objects.create(
            room_type="single",
            number="101",
            name="Room A",
            description="Nice room with sea view",
            price="100",
            capacity=2,
            amenities=[{"name": "WiFi"}, {"name": "TV"}],
        )

        self.guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
        )

        # Existing booking for conflict test
        self.booking = Booking.objects.create(
            room=self.room,
            check_in=datetime.date(2025, 9, 1),
            check_out=datetime.date(2025, 9, 5),
            guest=self.guest,
            status="CONFIRMED",
            total_price="500",
            payment_status="PENDING",
        )

    # ---------------- ROOM TESTS ----------------
    def test_create_room_via_api(self):
        url = reverse("room-list")
        payload = {
            "amenities": [{"name": "WiFi"}, {"name": "Air Conditioning"}],
            "room_type": "double",
            "number": "102",
            "name": "Room B",
            "description": "Luxury room",
            "price": "200",
            "capacity": 3,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Room B")
        self.assertEqual(response.data["capacity"], 3)
        self.assertEqual(
            response.data["amenities"], [{"name": "WiFi"}, {"name": "Air Conditioning"}]
        )

    def test_create_room_invalid_capacity(self):
        url = reverse("room-list")
        payload = {
            "amenities": [{"name": "WiFi"}],
            "room_type": "single",
            "number": "103",
            "name": "Room C",
            "description": "Test room",
            "price": "150",
            "capacity": 0,  # Invalid
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------------- BOOKING TESTS ----------------
    def test_double_booking_conflict(self):
        url = reverse("booking-list")
        payload = {
            "room": self.room.id,
            "guest": {
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "bob@example.com",
                "phone": "123456789",
            },
            "check_in": "2025-09-03",
            "check_out": "2025-09-06",
            "status": "CONFIRMED",
            "total_price": "300",
            "payment_status": "PENDING",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("Room is already booked" in str(response.data))

    def test_non_conflicting_booking(self):
        url = reverse("booking-list")
        payload = {
            "room": self.room.id,
            "guest": {
                "first_name": "Charlie",
                "last_name": "Brown",
                "email": "charlie@example.com",
                "phone": "987654321",
            },
            "check_in": "2025-09-06",
            "check_out": "2025-09-10",
            "status": "CONFIRMED",
            "total_price": "400",
            "payment_status": "PENDING",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
