from django.contrib import admin
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog
admin.site.register(Payment)
admin.site.register(PaymentReceipt)
admin.site.register(PaymentGatewayWebhookLog)
