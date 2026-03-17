from django.contrib import admin
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog, UtilityBill
admin.site.register(Payment)
admin.site.register(PaymentReceipt)
admin.site.register(PaymentGatewayWebhookLog)
admin.site.register(UtilityBill)
