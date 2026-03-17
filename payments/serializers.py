from rest_framework import serializers
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog, UtilityBill

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at']

class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = '__all__'
        read_only_fields = ['receipt_number', 'created_at']

class WebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayWebhookLog
        fields = '__all__'

class UtilityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityBill
        fields = '__all__'
        read_only_fields = ['created_at']
