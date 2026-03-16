from rest_framework import serializers
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog


class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = ('id', 'receipt_number', 'generated_at', 'pdf_file')
        read_only_fields = ('id', 'receipt_number', 'generated_at')


class PaymentSerializer(serializers.ModelSerializer):
    receipt = PaymentReceiptSerializer(read_only=True)
    tenant_email = serializers.CharField(source='tenant.email', read_only=True)
    lease_info = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'tenant', 'tenant_email', 'lease', 'lease_info', 'amount',
                  'payment_date', 'payment_method', 'status', 'transaction_id',
                  'gateway_response', 'receipt', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_lease_info(self, obj):
        return {
            'id': obj.lease.id,
            'room': obj.lease.room.room_number,
            'building': obj.lease.room.building.name,
        }


class PaymentGatewayWebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayWebhookLog
        fields = ('id', 'gateway', 'event_type', 'payload', 'processed', 'created_at')
        read_only_fields = ('id', 'created_at')
