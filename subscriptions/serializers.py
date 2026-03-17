from rest_framework import serializers
from .models import Subscription, SubscriptionInvoice


class SubscriptionInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionInvoice
        fields = '__all__'
        read_only_fields = ['invoice_number', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    monthly_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    invoices = SubscriptionInvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['owner', 'price_per_room', 'created_at', 'updated_at']
