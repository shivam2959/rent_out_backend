from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('deposit', 'Security Deposit'),
        ('maintenance', 'Maintenance Charge'),
        ('fine', 'Fine/Penalty'),
        ('other', 'Other'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('cheque', 'Cheque'),
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    lease = models.ForeignKey('leases.LeaseAgreement', on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True)
    gateway_payment_id = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id}: {self.tenant.email} - {self.amount}"


class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    receipt_document = models.FileField(upload_to='receipts/', null=True, blank=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"RCP-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_number}"


class PaymentGatewayWebhookLog(models.Model):
    GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
    ]

    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    processed = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook {self.gateway} - {self.event_type}"
