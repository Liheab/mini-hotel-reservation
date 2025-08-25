from django.db import models


class Status(models.TextChoices):
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    PENDING = "PENDING", "Pending"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


class RoomType(models.TextChoices):
    SINGLE = "single", "Single"
    DOUBLE = "double", "Double"
