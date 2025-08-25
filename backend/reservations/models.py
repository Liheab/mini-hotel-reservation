from django.db import models
from reservations.constants import RoomType, Status, PaymentStatus


class Room(models.Model):

    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True)
    room_type = models.CharField(max_length=10, choices=RoomType)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(default=1)
    amenities = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"


class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.CONFIRMED
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.room} ({self.check_in} to {self.check_out})"

    def save(self, *args, **kwargs):
        # Auto-calculate total price if not provided
        if not self.total_price:
            days = (self.check_out - self.check_in).days
            days = max(days, 1)
            self.total_price = self.room.price * days
            self.room.is_available = False
            self.room.save(update_fields=["is_available"])
        super().save(*args, **kwargs)
