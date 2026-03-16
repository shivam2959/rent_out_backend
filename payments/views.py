from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog
from .serializers import PaymentSerializer, PaymentReceiptSerializer, PaymentGatewayWebhookLogSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['tenant__email', 'transaction_id']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    filterset_fields = ['status', 'payment_type', 'payment_method']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all().select_related('tenant', 'lease')
        return Payment.objects.filter(
            Q(tenant=user) | Q(lease__room__building__owner=user)
        ).select_related('tenant', 'lease')

    def perform_create(self, serializer):
        payment = serializer.save(tenant=self.request.user)
        if payment.status == 'completed':
            PaymentReceipt.objects.get_or_create(payment=payment)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.save()
        receipt, _ = PaymentReceipt.objects.get_or_create(payment=payment)
        return Response({'status': 'completed', 'receipt_number': receipt.receipt_number})


class PaymentReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentReceipt.objects.all()
    serializer_class = PaymentReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PaymentReceipt.objects.all()
        return PaymentReceipt.objects.filter(
            Q(payment__tenant=user) | Q(payment__lease__room__building__owner=user)
        )


class PaymentGatewayWebhookLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentGatewayWebhookLog.objects.all()
    serializer_class = PaymentGatewayWebhookLogSerializer
    permission_classes = [permissions.IsAdminUser]
