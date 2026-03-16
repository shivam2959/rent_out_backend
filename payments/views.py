from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog
from .serializers import PaymentSerializer, PaymentReceiptSerializer, PaymentGatewayWebhookLogSerializer
from users.permissions import IsOwnerOrAdmin


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.select_related('tenant', 'lease__room__building').all()
        if user.role == 'owner':
            return Payment.objects.select_related('tenant', 'lease__room__building').filter(lease__owner=user)
        return Payment.objects.select_related('tenant', 'lease__room__building').filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'], url_path='generate-receipt')
    def generate_receipt(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'completed':
            return Response(
                {'error': 'Can only generate receipt for completed payments.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        receipt, created = PaymentReceipt.objects.get_or_create(payment=payment)
        return Response(PaymentReceiptSerializer(receipt).data)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        queryset = self.get_queryset()
        from django.db.models import Sum
        from django.utils import timezone
        now = timezone.now()
        data = {
            'total_payments': queryset.count(),
            'completed_payments': queryset.filter(status='completed').count(),
            'pending_payments': queryset.filter(status='pending').count(),
            'total_amount': queryset.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0,
            'this_month': queryset.filter(
                status='completed',
                payment_date__year=now.year,
                payment_date__month=now.month
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return Response(data)


class PaymentGatewayWebhookViewSet(viewsets.ModelViewSet):
    queryset = PaymentGatewayWebhookLog.objects.all()
    serializer_class = PaymentGatewayWebhookLogSerializer
    permission_classes = [IsAdminUser]
