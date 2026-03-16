from django.contrib import admin
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tenant', 'amount', 'payment_type', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_type', 'payment_method']
    search_fields = ['tenant__email', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'payment', 'issued_at']
    search_fields = ['receipt_number', 'payment__tenant__email']
    readonly_fields = ['receipt_number', 'issued_at']


@admin.register(PaymentGatewayWebhookLog)
class PaymentGatewayWebhookLogAdmin(admin.ModelAdmin):
    list_display = ['gateway', 'event_type', 'processed', 'received_at']
    list_filter = ['gateway', 'processed']
    readonly_fields = ['received_at']
