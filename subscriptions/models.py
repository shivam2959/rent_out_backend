import uuid
from decimal import Decimal
from django.db import models
from users.models import CustomUser


PRICE_PER_ROOM = Decimal('50.00')


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('cancelled', 'Cancelled'),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    active_room_count = models.PositiveIntegerField(default=0)
    price_per_room = models.DecimalField(max_digits=8, decimal_places=2, default=PRICE_PER_ROOM)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def monthly_amount(self):
        return self.active_room_count * self.price_per_room

    def __str__(self):
        return f"Subscription for {self.owner.username} – {self.active_room_count} rooms – ₹{self.monthly_amount}"


class SubscriptionInvoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} – ₹{self.amount} ({self.status})"
