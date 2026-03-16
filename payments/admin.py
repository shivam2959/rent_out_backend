from django.contrib import admin
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('tenant__email', 'transaction_id')
    ordering = ('-created_at',)


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'payment', 'generated_at')
    search_fields = ('receipt_number', 'payment__tenant__email')


@admin.register(PaymentGatewayWebhookLog)
class PaymentGatewayWebhookLogAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'event_type', 'processed', 'created_at')
    list_filter = ('gateway', 'processed')
