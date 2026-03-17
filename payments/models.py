import uuid
from django.db import models
from leases.models import LeaseAgreement
from properties.models import Room

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('other', 'Other'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('deposit', 'Security Deposit'),
        ('maintenance_fee', 'Maintenance Fee'),
        ('penalty', 'Late Penalty'),
        ('utility', 'Utility Bill'),
        ('subscription', 'Subscription'),
        ('commission', 'Broker Commission'),
        ('other', 'Other'),
    ]
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='rent')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} – {self.payment_type} – {self.amount} ({self.status})"


class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"REC-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_number}"


class PaymentGatewayWebhookLog(models.Model):
    gateway = models.CharField(max_length=50)
    payload = models.JSONField()
    status = models.CharField(max_length=20, default='received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook from {self.gateway} at {self.created_at}"


class UtilityBill(models.Model):
    BILL_TYPE_CHOICES = [
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='utility_bills')
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES)
    bill_month = models.DateField(help_text="First day of the billing month")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_bill_type_display()} bill for Room {self.room.room_number} – {self.bill_month}"
