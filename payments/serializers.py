from rest_framework import serializers
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog


class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = '__all__'
        read_only_fields = ['receipt_number', 'issued_at']


class PaymentSerializer(serializers.ModelSerializer):
    receipt = PaymentReceiptSerializer(read_only=True)
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at', 'updated_at']


class PaymentGatewayWebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayWebhookLog
        fields = '__all__'
        read_only_fields = ['received_at']
