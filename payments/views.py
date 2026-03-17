from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment, PaymentReceipt, PaymentGatewayWebhookLog, UtilityBill
from .serializers import PaymentSerializer, PaymentReceiptSerializer, WebhookLogSerializer, UtilityBillSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return Payment.objects.filter(lease__owner=user)
        return Payment.objects.filter(lease__tenant=user)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.save()
        receipt, _ = PaymentReceipt.objects.get_or_create(payment=payment)
        return Response({
            'payment': PaymentSerializer(payment).data,
            'receipt': PaymentReceiptSerializer(receipt).data,
        })

class PaymentReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return PaymentReceipt.objects.filter(payment__lease__owner=user)
        return PaymentReceipt.objects.filter(payment__lease__tenant=user)

class WebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        log = PaymentGatewayWebhookLog.objects.create(
            gateway=request.headers.get('X-Gateway', 'unknown'),
            payload=request.data,
        )
        return Response({'id': log.id}, status=status.HTTP_200_OK)

class UtilityBillViewSet(viewsets.ModelViewSet):
    serializer_class = UtilityBillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return UtilityBill.objects.filter(room__building__owner=user)
        return UtilityBill.objects.filter(room__leases__tenant=user, room__leases__status='active').distinct()
