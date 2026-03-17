from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from properties.models import Room
from .models import Subscription, SubscriptionInvoice, PRICE_PER_ROOM
from .serializers import SubscriptionSerializer, SubscriptionInvoiceSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Subscription.objects.all()
        return Subscription.objects.filter(owner=user)

    def perform_create(self, serializer):
        import calendar
        user = self.request.user
        active_rooms = Room.objects.filter(
            building__owner=user, is_available=False
        ).count()
        today = timezone.now().date()
        last_day = calendar.monthrange(today.year, today.month)[1]
        billing_start = today.replace(day=1)
        billing_end = today.replace(day=last_day)
        serializer.save(
            owner=user,
            active_room_count=active_rooms,
            price_per_room=PRICE_PER_ROOM,
            billing_period_start=billing_start,
            billing_period_end=billing_end,
        )

    @action(detail=True, methods=['post'])
    def sync_room_count(self, request, pk=None):
        """Recalculate active_room_count from actual occupied rooms."""
        sub = self.get_object()
        active_rooms = Room.objects.filter(
            building__owner=sub.owner, is_available=False
        ).count()
        sub.active_room_count = active_rooms
        sub.save()
        return Response(SubscriptionSerializer(sub).data)

    @action(detail=True, methods=['post'])
    def generate_invoice(self, request, pk=None):
        """Generate a monthly invoice for this subscription."""
        sub = self.get_object()
        today = timezone.now().date()
        # Due date is the 7th of next month
        if today.month == 12:
            due = today.replace(year=today.year + 1, month=1, day=7)
        else:
            due = today.replace(month=today.month + 1, day=7)
        invoice = SubscriptionInvoice.objects.create(
            subscription=sub,
            amount=sub.monthly_amount,
            due_date=due,
            status='issued',
        )
        return Response(SubscriptionInvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)


class SubscriptionInvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionInvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return SubscriptionInvoice.objects.all()
        return SubscriptionInvoice.objects.filter(subscription__owner=user)
